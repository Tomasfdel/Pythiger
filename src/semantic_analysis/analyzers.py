from typing import Set, Optional, Union, List

from dataclasses import dataclass

import parser.ast_nodes as ast
from intermediate_representation.translated_expression import TranslatedExpression
from semantic_analysis.environment import EnvironmentEntry, VariableEntry, FunctionEntry
from semantic_analysis.table import SymbolTable
from semantic_analysis.types import (
    Type,
    NameType,
    ArrayType,
    RecordType,
    Field,
    IntType,
    NilType,
    StringType,
    are_types_equal,
    VoidType,
)


@dataclass
class TypedExpression:
    expression: TranslatedExpression
    type: Type


class SemanticError(Exception):
    def __init__(self, message: str, position: int):
        self.message = message
        self.position = position

    def __str__(self):
        return f"Compilation error! {self.message} in line {self.position}"


def simplify_type_aliases(
    type_name: str, type_env: SymbolTable[Type], already_seen: Set[str]
) -> Optional[Type]:
    """Goes through a chain of type aliases and makes them all point to the referenced type.

    This function recursively moves through the chain, keeping track of already seen type aliases.
    If at some point it sees one that has already been visited, it detects a loop and returns None.
    If not, it eventually finds a record or array definition, and goes back the chain updating all
    visited type aliases so they point to the corresponding type."""

    if type_name in already_seen:
        return None
    type_definition = type_env.find(type_name)
    if isinstance(type_definition, NameType):
        already_seen.add(type_name)
        alias_type = simplify_type_aliases(
            type_definition.symbol, type_env, already_seen
        )
        if alias_type is not None:
            type_env.add(type_name, alias_type)
        return alias_type
    return type_definition


def maybe_lookup_name_type(type_definition: Type, type_env: SymbolTable[Type]) -> Type:
    """If the given type is a name reference, returns the referenced type."""

    if isinstance(type_definition, NameType):
        return type_env.find(type_definition.symbol)
    return type_definition


def eliminate_name_types(type_definition: Type, type_env: SymbolTable[Type]):
    """Given an array of record type definition, eliminates all its name references."""

    if isinstance(type_definition, ArrayType):
        type_definition.type = maybe_lookup_name_type(type_definition.type, type_env)
    if isinstance(type_definition, RecordType):
        type_definition.fields = [
            Field(field.name, maybe_lookup_name_type(field.type, type_env))
            for field in type_definition.fields
        ]


def check_name_unicity(
    declaration_list: Union[List[ast.FunctionDec], List[ast.TypeDec]]
) -> bool:
    """Checks if all names in a function or type declaration block are unique."""

    seen_names = set()
    for declaration in declaration_list:
        if declaration.name in seen_names:
            return False
        seen_names.add(declaration.name)
    return True


def translate_variable(
    value_env: SymbolTable[EnvironmentEntry],
    type_env: SymbolTable[Type],
    variable: ast.Variable,
) -> TypedExpression:
    if isinstance(variable, ast.SimpleVar):
        # Simple variable: Look it up in the value environment.
        var_value = value_env.find(variable.sym)
        if var_value is None or not isinstance(var_value, VariableEntry):
            raise SemanticError(f"Undefined variable {variable.sym}", variable.position)
        return TypedExpression(TranslatedExpression(), var_value.type)

    if isinstance(variable, ast.FieldVar):
        # Record field: Look up the variable, check it's a record and that it has the given field.
        trans_var = translate_variable(value_env, type_env, variable.var)
        if not isinstance(trans_var.type, RecordType):
            raise SemanticError(
                f"Trying to access the {variable.sym} field of a variable that is not a record",
                variable.var.position,
            )
        for field in trans_var.type.fields:
            if field.name == variable.sym:
                return TypedExpression(TranslatedExpression(), field.type)
        raise SemanticError(
            f"Unknown record field name {variable.sym} for variable",
            variable.var.position,
        )

    if isinstance(variable, ast.SubscriptVar):
        # Array subscript: Look up the variable, check it's a record and that the subscript
        # expression has integer type.
        trans_var = translate_variable(value_env, type_env, variable.var)
        if not isinstance(trans_var.type, ArrayType):
            raise SemanticError(
                "Trying to access a subscript of a variable that is not an array",
                variable.var.position,
            )
        trans_exp = translate_expression(value_env, type_env, variable.exp)
        if not isinstance(trans_exp.type, IntType):
            raise SemanticError(
                "Array subscript must be an Integer", variable.exp.position
            )
        return TypedExpression(TranslatedExpression(), trans_var.type.type)

    raise SemanticError("Unknown variable kind", variable.position)


def translate_expression(
    value_env: SymbolTable[EnvironmentEntry],
    type_env: SymbolTable[Type],
    expression: ast.Expression,
) -> TypedExpression:
    if isinstance(expression, ast.VarExp):
        # Variable name: Translate the variable and return that value.
        return translate_variable(value_env, type_env, expression.var)

    if isinstance(expression, ast.NilExp):
        # Nil constant: Return nil type.
        return TypedExpression(TranslatedExpression(), NilType())

    if isinstance(expression, ast.IntExp):
        # Integer constant: Return integer type.
        return TypedExpression(TranslatedExpression(), IntType())

    if isinstance(expression, ast.StringExp):
        # String constant: Return string type.
        return TypedExpression(TranslatedExpression(), StringType())

    if isinstance(expression, ast.CallExp):
        # Function call: Look up the function name, check the types of the parameters and return
        # its return value type.
        func_value = value_env.find(expression.func)
        if func_value is None:
            raise SemanticError(
                f"Undefined function {expression.func}", expression.position
            )
        if not isinstance(func_value, FunctionEntry):
            raise SemanticError(
                f"Non-function value {expression.func} is not callable",
                expression.position,
            )
        if len(expression.args) != len(func_value.formals):
            raise SemanticError(
                f"Wrong number of arguments in function call to {expression.func},"
                + f" {len(func_value.formals)} expected, but {len(expression.args)} given",
                expression.position,
            )
        for arg_position in range(len(expression.args)):
            trans_exp = translate_expression(
                value_env, type_env, expression.args[arg_position]
            )
            if not are_types_equal(func_value.formals[arg_position], trans_exp.type):
                raise SemanticError(
                    f"Wrong type for argument in position {arg_position}"
                    + f" in call to {expression.func}",
                    expression.position,
                )
        return TypedExpression(TranslatedExpression(), func_value.result)

    if isinstance(expression, ast.OpExp):
        # Operation: If an arithmetic operation, check if both values are Integers.
        # If an in/equality comparison, check if both values have the same type.
        # If an order comparison, check if both values are either Integers or Strings.
        left = translate_expression(value_env, type_env, expression.left)
        right = translate_expression(value_env, type_env, expression.right)
        if expression.oper in (
            ast.Oper.plus,
            ast.Oper.minus,
            ast.Oper.times,
            ast.Oper.divide,
        ):
            if not isinstance(left.type, IntType):
                raise SemanticError(
                    "Left arithmetic operand must be an Integer",
                    expression.left.position,
                )
            if not isinstance(right.type, IntType):
                raise SemanticError(
                    "Right arithmetic operand must be an Integer",
                    expression.right.position,
                )
        elif expression.oper in (
            ast.Oper.eq,
            ast.Oper.neq,
            ast.Oper.lt,
            ast.Oper.le,
            ast.Oper.gt,
            ast.Oper.ge,
        ):
            if not are_types_equal(left.type, right.type):
                raise SemanticError(
                    "Values must be of the same type to test for equality or order",
                    expression.position,
                )
            if expression.oper in (
                ast.Oper.lt,
                ast.Oper.le,
                ast.Oper.gt,
                ast.Oper.ge,
            ) and not (
                are_types_equal(left.type, IntType())
                or are_types_equal(left.type, StringType())
            ):
                raise SemanticError(
                    "Values must be Integers or Strings to compare their order",
                    expression.position,
                )
        else:
            raise SemanticError("Unknown operator", expression.position)
        return TypedExpression(TranslatedExpression(), IntType())

    if isinstance(expression, ast.RecordExp):
        # Record creation: Check the type is a record type, that only and all its defined fields
        # are declared and that all their associated expressions have the declared type.
        trans_typ = type_env.find(expression.type)
        if trans_typ is None:
            raise SemanticError(
                f"Undefined record type {expression.type}",
                expression.position,
            )
        if not isinstance(trans_typ, RecordType):
            raise SemanticError(
                f"Trying to create a record of type {expression.type}, which is not a record type",
                expression.position,
            )
        checked_fields = set()
        for exp_field in expression.fields:
            if exp_field.name in checked_fields:
                raise SemanticError(
                    f"Repeated field assignment for field {exp_field.name} in record creation",
                    exp_field.position,
                )
            found_field = False
            expected_field_type = None
            for type_field in trans_typ.fields:
                if type_field.name == exp_field.name:
                    found_field = True
                    expected_field_type = type_field.type
                    checked_fields.add(exp_field.name)
                    break
            if not found_field:
                raise SemanticError(
                    f"Unknown field {exp_field.name} in record creation",
                    exp_field.position,
                )
            trans_exp = translate_expression(value_env, type_env, exp_field.exp)
            if not are_types_equal(expected_field_type, trans_exp.type):
                raise SemanticError(
                    f"Assigning value of a wrong type to field {exp_field.name} in record creation",
                    exp_field.exp.position,
                )
        if len(checked_fields) < len(trans_typ.fields):
            raise SemanticError(
                "Missing field assignment in record creation",
                expression.position,
            )
        return TypedExpression(TranslatedExpression(), trans_typ)

    if isinstance(expression, ast.SeqExp):
        # Sequence of expressions: Evaluate each of them and return the type of the last one.
        trans_exp = TypedExpression(TranslatedExpression(), VoidType())
        for seq_expression in expression.seq:
            trans_exp = translate_expression(value_env, type_env, seq_expression)
        return trans_exp

    if isinstance(expression, ast.AssignExp):
        # Assignment: Look up the l-value, make sure it's not a loop variable and that the
        # expression and l-value types match.
        if isinstance(expression.var, ast.SimpleVar):
            var_entry = value_env.find(expression.var.sym)
            if var_entry is None:
                raise SemanticError(
                    f"Trying to assign a value to undefined variable {expression.var.sym}",
                    expression.var.position,
                )
            if isinstance(var_entry, VariableEntry) and not var_entry.is_editable:
                raise SemanticError(
                    f"For loop variable {expression.var.sym} is not assignable",
                    expression.var.position,
                )
        trans_var = translate_variable(value_env, type_env, expression.var)
        trans_exp = translate_expression(value_env, type_env, expression.exp)
        if not are_types_equal(trans_var.type, trans_exp.type):
            raise SemanticError(
                "Trying to assign a value to a variable of a different type",
                expression.position,
            )
        return TypedExpression(TranslatedExpression(), VoidType())

    if isinstance(expression, ast.IfExp):
        # If: Check the conditional expression returns an Integer type.
        # If it only has a then branch, then check it produces no value and return no value.
        # If it also has an else branch. make sure both produce the same type and return it.
        trans_test = translate_expression(value_env, type_env, expression.test)
        if not isinstance(trans_test.type, IntType):
            raise SemanticError(
                "The condition of an If expression must be an Integer",
                expression.test.position,
            )
        trans_then = translate_expression(value_env, type_env, expression.thenDo)
        if expression.elseDo is None:
            if not isinstance(trans_then.type, VoidType):
                raise SemanticError(
                    "Then branch of an If expression must produce no value"
                    + " when there is no Else branch",
                    expression.thenDo.position,
                )
            return TypedExpression(TranslatedExpression(), VoidType())
        trans_else = translate_expression(value_env, type_env, expression.elseDo)
        if not are_types_equal(trans_then.type, trans_else.type):
            raise SemanticError(
                "Then and Else branches of an If expression must return values of the same type",
                expression.position,
            )
        # Special check in case one of the branches returns NilType and the other a RecordType.
        # In that case, we should return the RecordType since it's the most generic one.
        if isinstance(trans_then.type, NilType):
            returned_type = trans_else.type
        else:
            returned_type = trans_then.type
        return TypedExpression(TranslatedExpression(), returned_type)

    if isinstance(expression, ast.WhileExp):
        # While: Check that the condition is an Integer and that the body produces no value.
        trans_test = translate_expression(value_env, type_env, expression.test)
        if not isinstance(trans_test.type, IntType):
            raise SemanticError(
                "The condition of a While expression must be an Integer",
                expression.position,
            )
        value_env.begin_scope(True)
        type_env.begin_scope(True)
        trans_body = translate_expression(value_env, type_env, expression.body)
        if not isinstance(trans_body.type, VoidType):
            raise SemanticError(
                "While body must produce no value", expression.body.position
            )
        value_env.end_scope()
        type_env.end_scope()
        return TypedExpression(TranslatedExpression(), VoidType())

    if isinstance(expression, ast.BreakExp):
        # Break: Make sure that the closest scope start is a While or a For loop.
        if not value_env.is_closest_scope_a_loop():
            raise SemanticError(
                "Break expression must be inside a For or While loop",
                expression.position,
            )
        return TypedExpression(TranslatedExpression(), VoidType())

    if isinstance(expression, ast.ForExp):
        # For: Check that ends of the for variable iteration are Integers. Then add a non editable
        # Integer variable to the value env and evaluate the body, making sure it produces no value.
        trans_lo = translate_expression(value_env, type_env, expression.lo)
        if not isinstance(trans_lo.type, IntType):
            raise SemanticError(
                "Starting value for loop variable in a For expression must be an Integer",
                expression.lo.position,
            )
        trans_hi = translate_expression(value_env, type_env, expression.hi)
        if not isinstance(trans_hi.type, IntType):
            raise SemanticError(
                "Ending value for loop variable in a For expression must be an Integer",
                expression.hi.position,
            )
        value_env.begin_scope(True)
        type_env.begin_scope(True)
        value_env.add(expression.var, VariableEntry(IntType(), False))
        trans_body = translate_expression(value_env, type_env, expression.body)
        if not isinstance(trans_body.type, VoidType):
            raise SemanticError(
                "For body must produce no value", expression.body.position
            )
        value_env.end_scope()
        type_env.end_scope()
        return TypedExpression(TranslatedExpression(), VoidType())

    if isinstance(expression, ast.LetExp):
        # Let: Go through all declarations and then evaluate the body of the expression. The return
        # type is the one of the last expression in the body (or Void if there are none)
        value_env.begin_scope()
        type_env.begin_scope()
        for declaration in expression.decs.declarationList:
            translate_declaration(value_env, type_env, declaration)
        trans_exp = translate_expression(value_env, type_env, expression.body)
        value_env.end_scope()
        type_env.end_scope()
        return trans_exp

    if isinstance(expression, ast.ArrayExp):
        # Array creation: Check that the declared type is an array type, that the size is an Integer
        # and that the initial value is of the type of the elements of the array.
        trans_typ = type_env.find(expression.type)
        if trans_typ is None:
            raise SemanticError(
                f"Undefined array type {expression.type}",
                expression.position,
            )
        if not isinstance(trans_typ, ArrayType):
            raise SemanticError(
                f"Trying to create an array of type {expression.type}, which is not an array type",
                expression.position,
            )
        trans_size = translate_expression(value_env, type_env, expression.size)
        if not isinstance(trans_size.type, IntType):
            raise SemanticError(
                "Array size must be an Integer", expression.size.position
            )
        trans_init = translate_expression(value_env, type_env, expression.init)
        if not are_types_equal(trans_typ.type, trans_init.type):
            raise SemanticError(
                "Array initial value must be of its declared type",
                expression.init.position,
            )
        return TypedExpression(TranslatedExpression(), trans_typ)

    if isinstance(expression, ast.EmptyExp):
        return TypedExpression(TranslatedExpression(), VoidType())

    raise SemanticError("Unknown expression kind", expression.position)


def translate_declaration(
    value_env: SymbolTable[EnvironmentEntry],
    type_env: SymbolTable[Type],
    declaration: ast.Declaration,
):
    if isinstance(declaration, ast.FunctionDecBlock):
        # Function declaration block: Check that all function names are unique. Then, evaluate each
        # function header and add it to the value environment. Then, for each function, push its
        # parameters to the value environment and make sure the function body returns the same type
        # as the declared one.
        if not check_name_unicity(declaration.functionDecList):
            raise SemanticError(
                "All names in the function declaration block must be unique",
                declaration.position,
            )
        function_entries = []
        for function_dec in declaration.functionDecList:
            formals = []
            for parameter in function_dec.params:
                param_type = type_env.find(parameter.type)
                if param_type is None:
                    raise SemanticError(
                        f"Undefined argument type {parameter.type} for parameter {parameter.name}"
                        + f"in function {function_dec.name}",
                        parameter.position,
                    )
                formals.append(param_type)
            if function_dec.returnType is None:
                return_type = VoidType()
            else:
                return_type = type_env.find(function_dec.returnType)
                if return_type is None:
                    raise SemanticError(
                        f"Undefined return type {function_dec.returnType}"
                        + f" for function {function_dec.name}",
                        function_dec.position,
                    )
            function_entry = FunctionEntry(formals, return_type)
            function_entries.append(function_entry)
            value_env.add(function_dec.name, function_entry)
        for function_dec, function_entry in zip(
            declaration.functionDecList, function_entries
        ):
            value_env.begin_scope()
            for param, formal_type in zip(function_dec.params, function_entry.formals):
                value_env.add(param.name, VariableEntry(formal_type))
            trans_exp = translate_expression(value_env, type_env, function_dec.body)
            if not are_types_equal(trans_exp.type, function_entry.result):
                raise SemanticError(
                    f"Function {function_dec.name} returns a value of a type"
                    + " different than its declared type",
                    function_dec.position,
                )
            value_env.end_scope()

    elif isinstance(declaration, ast.VariableDec):
        # Variable declaration: Translate the expression, make sure its type matches the declared
        # type and that a variable initialized to nil has a type declaration of a record type.
        trans_exp = translate_expression(value_env, type_env, declaration.exp)
        if isinstance(trans_exp.type, NilType) and declaration.type is None:
            raise SemanticError(
                f"Must declare the type of variable {declaration.name} when initializing it to nil",
                declaration.position,
            )
        if declaration.type is not None:
            declared_type = type_env.find(declaration.type)
            if declared_type is None:
                raise SemanticError(
                    f"Undefined type {declaration.type} in variable declaration"
                    + f" for {declaration.name}",
                    declaration.position,
                )
            if isinstance(trans_exp.type, NilType) and not isinstance(
                declared_type, RecordType
            ):
                raise SemanticError(
                    f"Variable {declaration.name} must be of a record type when initialized to nil",
                    declaration.position,
                )
            if not are_types_equal(declared_type, trans_exp.type):
                raise SemanticError(
                    f"Initial value for variable {declaration.name} is not of its"
                    + f" declared type {declaration.type}",
                    declaration.position,
                )
            value_env.add(declaration.name, VariableEntry(declared_type))
        value_env.add(declaration.name, VariableEntry(trans_exp.type))

    elif isinstance(declaration, ast.TypeDecBlock):
        # Type declaration block: Check that all type names are unique. Then, follow these steps:
        # - Add a dummy reference to the type environment for every type declaration, so as to be
        # able to recognize undefined types in the following step.
        # - Translate each type and add it to the type environment. In this step, references to
        # types in the same block are stored as a name reference and not as a pointer to the real
        # referenced type.
        # - For each definition that is a type alias (the name we give to those that just name
        # another type instead of creating a record or array), keep moving forward in the type
        # aliases chain until you find a record or array type. Then make all involved type aliases
        # point to that record or array type. If you only find type aliases, you are inside a loop,
        # so return an error once you detect it.
        # - Go through all types again and, now that all type aliases are eliminated and point
        # at the right type definition, eliminate any name type references left by replacing them
        # with a pointer to the right type.
        # This implementation is not optimized at all, but It Just Works(TM) and we found it easier
        # to follow than the one in the book.
        if not check_name_unicity(declaration.typeDecList):
            raise SemanticError(
                "All names in the type declaration block must be unique",
                declaration.position,
            )
        for type_dec in declaration.typeDecList:
            type_env.add(type_dec.name, NameType(type_dec.name))
        for type_dec in declaration.typeDecList:
            type_env.add(type_dec.name, translate_type(type_env, type_dec.type))
        for type_dec in declaration.typeDecList:
            if simplify_type_aliases(type_dec.name, type_env, set()) is None:
                raise SemanticError(
                    f"Cyclic type definition found involving type {type_dec.name}",
                    type_dec.position,
                )
        for type_dec in declaration.typeDecList:
            type_definition = type_env.find(type_dec.name)
            eliminate_name_types(type_definition, type_env)

    else:
        raise SemanticError("Unknown declaration kind", declaration.position)


def translate_type(type_env: SymbolTable[Type], ty: ast.Type) -> Type:
    if isinstance(ty, ast.NameTy):
        # Named type: Look it up in the type environment.
        type_value = type_env.find(ty.name)
        if type_value is None:
            raise SemanticError(f"Undefined type name {ty.name}", ty.position)
        return type_value

    if isinstance(ty, ast.RecordTy):
        # Record type: Look up every field type while building the field list.
        field_list = []
        for field in ty.fieldList:
            type_value = type_env.find(field.type)
            if type_value is None:
                raise SemanticError(
                    f"Undefined record field type {field.type}", field.position
                )
            field_list.append(Field(field.name, type_value))
        return RecordType(field_list)

    if isinstance(ty, ast.ArrayTy):
        # Array type: Look of the elements type and build the array type.
        type_value = type_env.find(ty.array)
        if type_value is None:
            raise SemanticError(f"Undefined array element type {ty.array}", ty.position)
        return ArrayType(type_value)

    raise SemanticError("Unknown type kind", ty.position)
