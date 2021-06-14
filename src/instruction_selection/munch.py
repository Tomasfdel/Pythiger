import intermediate_representation.tree as IRT
import assembly as Assembly

# TODO: Placeholder, not needed.
from activation_records.temp import temp_to_str


# TODO: No idea what this does (yet).
def emit(instruction: Assembly.Instruction) -> None:
    print(instruction.format(temp_to_str))


# x86-64
# AT&T syntax:
# instruction source, destination
# System V ABI


# TODO: Add exceptions.


# TODO: Ask tomasu if a dictionary here is fine.
comparison_operator_to_jump = {
    IRT.RelationalOperator.eq: "je",
    IRT.RelationalOperator.ne: "jne",
    IRT.RelationalOperator.lt: "jl",
    IRT.RelationalOperator.gt: "jg",
    IRT.RelationalOperator.le: "jle",
    IRT.RelationalOperator.ge: "jge",
    IRT.RelationalOperator.ult: "jb",
    IRT.RelationalOperator.ule: "jbe",
    IRT.RelationalOperator.ugt: "ja",
    IRT.RelationalOperator.uge: "jae",
}


# TODO: Esto no devuelve None, pero por ahora no tenemos el arbol de assembly.
def munchStm(stmNode: IRT.Statement) -> None:
    if isinstance(stmNode, IRT.Label):
        # TODO: Verify if line is correct.
        emit(Assembly.Label(line=f"{stmNode.label}:", label=stmNode.label))

    # TODO: Why does IRT.Jump.expression exist?
    if isinstance(stmNode, IRT.Jump):
        emit(
            Assembly.Operation(
                line="jmp 'j0", source=[], destination=[], jump=stmNode.labels
            )
        )

    if isinstance(stmNode, IRT.ConditionalJump):
        # The jump itself checks the flags in the EFL register.
        # These are usually set with TEST or CMP.
        emit(
            Assembly.Operation(
                line="cmp 's0, 's1",
                source=[munchExp(stmNode.left), munchExp(stmNode.right)],
                destination=[],
                jump=[],
            )
        )
        emit(
            Assembly.Operation(
                line=f"{comparison_operator_to_jump[stmNode.operator]} 'j0",
                source=[],
                destination=[],
                # TODO: Why is the false label here as well?
                jump=[stmNode.true, stmNode.false],
            )
        )

    # if isinstance(stmNode, IRT.Move):
    #     emit("MOVE")
    #     munchExp(stmNode.temporary)
    #     munchExp(stmNode.expression)
    #
    # # TODO: Ask tomasu what this node is.
    # if isinstance(stmNode, IRT.StatementExpression):
    #     emit("STATEMENT_EXPRESSION")
    #     munchExp(stmNode.expression)


# TODO: Esto no devuelve None, pero por ahora no tenemos el arbol de assembly.
def munchExp(expNode: IRT.Expression) -> None:
    pass
    # if isinstance(expNode, IRT.BinaryOperation):
    #     # TODO: Be careful if patterns differ by operator. There is no operator check here.
    #     emit(f"BINARY_OPERATION_WITH_{expNode.operator}")
    #     munchExp(expNode.left)
    #     munchExp(expNode.right)
    #
    # if isinstance(expNode, IRT.Memory):
    #     emit("MEMORY")
    #     munchExp(expNode.expression)
    #
    # if isinstance(expNode, IRT.Temporary):
    #     emit(f"TEMPORARY_{expNode.temporary}")
    #
    # if isinstance(expNode, IRT.Name):
    #     emit(expNode.label)
    #
    # if isinstance(expNode, IRT.Constant):
    #     emit(f"CONSTANT_{expNode.value}")
    #
    # if isinstance(expNode, IRT.Call):
    #     # function = munchExp(expNode.function)
    #     # arguments = [munchExp(argument) for argument in expNode.arguments]
    #     emit("CALL")
    #     munchExp(expNode.function)
    #     for argument in expNode.arguments:
    #         munchExp(argument)
    #
    # # TODO: Ask tomasu what this is.
    # if isinstance(expNode, IRT.Condition):
    #     emit("CONDITION")
    #     munchStm(statement)
