import intermediate_representation.tree as IRT
import assembly as Assembly
import activation_records.temp as Temp
import activation_records.frame as Frame
from typing import List

# TODO: Placeholder, not needed.
from activation_records.temp import temp_to_str


# TODO: No idea what this does (yet).
def emit(instruction: Assembly.Instruction) -> None:
    print(instruction.format(temp_to_str))


# x86-64
# AT&T syntax:
# instruction source, destination
# System V ABI

# Addressing modes for source operands in 'mov src, dst'
# $val: is a constant value
# %R: is a register
# 0xaddr: source read from Mem[0xaddr]
# (%R): source read from Mem[%R], where R is a register
# D(%R): source read from Mem[%R+D] where D is the displacement and R is a register


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
# There are two operators for multiplication and division, one for
# signed values and another for unsigned ones.
# Currently using signed version of mul and div.
binary_operator_to_use = {
    IRT.BinaryOperator.plus: "addq",
    IRT.BinaryOperator.minus: "subq",
    IRT.BinaryOperator.mul: "imulq",
    IRT.BinaryOperator.div: "idivq",
    IRT.BinaryOperator.andOp: "andq",
    IRT.BinaryOperator.orOp: "orq",
    IRT.BinaryOperator.lshift: "salq",
    IRT.BinaryOperator.rshift: "sarq",
    IRT.BinaryOperator.arshift: "shrq",
    IRT.BinaryOperator.xor: "xorq",
}


def munch_statement(stmNode: IRT.Statement) -> None:
    # Label(label): The constant value of name 'label', defined to be the current
    # machine code address.
    if isinstance(stmNode, IRT.Label):
        emit(Assembly.Label(line=f"{stmNode.label}:", label=stmNode.label))

    # TODO: Why does IRT.Jump.expression exist?
    # Jump (addr, labels): Transfer control to address 'addr'. The destination may
    # be a literal label, or it may be an address calculated by any other kind of expression.
    # The list of labels 'labels' specifies all possible locations that 'addr' may jump to.
    elif isinstance(stmNode, IRT.Jump):
        emit(
            Assembly.Operation(
                line="jmp 'j0", source=[], destination=[], jump=stmNode.labels
            )
        )
    # ConditionalJump(operator, exp_left, exp_right, true_label, false_label):
    # evaluate 'exp_left' and 'exp_right' in that order, yielding values 'a' and 'b'.
    # Then compare both values using 'operator'. If the result is TRUE, jump to 'true_label';
    # otherwise jump to 'false_label'.
    elif isinstance(stmNode, IRT.ConditionalJump):
        # The jump itself checks the flags in the EFL register.
        # These are usually set with TEST or CMP.
        emit(
            Assembly.Operation(
                line="cmpq %'s0, %'s1",
                source=[
                    munch_expression(stmNode.left),
                    munch_expression(stmNode.right),
                ],
                destination=[],
                jump=[],
            )
        )
        emit(
            Assembly.Operation(
                line=f"{comparison_operator_to_jump[stmNode.operator]} 'j0",
                source=[],
                destination=[],
                jump=[stmNode.true, stmNode.false],
            )
        )
    # Move(temporary, expression): we consider two different cases, based on the
    # content of 'temporary'.
    elif isinstance(stmNode, IRT.Move):
        # Warning: the IRT is built using the syntax as (move dst, src).
        # Here we swap the order of the expressions to match the AT&T syntax (move src, dst)

        # Move(Temporary t, exp): evaluates 'exp' and moves it to temporary 't'.
        if isinstance(stmNode.temporary, IRT.Temporary):
            emit(
                Assembly.Move(
                    line="movq %'s0, %'d0",
                    source=[munch_expression(stmNode.expression)],
                    destination=[munch_expression(stmNode.temporary)],
                )
            )
        elif isinstance(stmNode.temporary, IRT.Memory):
            # Move(mem(e1), e2): evaluates 'e1', yielding address 'addr'.
            # Then evaluate 'e2' and store the result into 'WordSize' bytes of memory
            # starting at 'addr'.
            emit(
                Assembly.Move(
                    line="movq %'s0, (%'s1)",
                    source=[
                        munch_expression(stmNode.expression),
                        munch_expression(stmNode.temporary.expression),
                    ],
                    destination=[],
                )
            )
        else:
            raise Exception("Munching an invalid version of node IRT.Move")
    # StatementExpression(exp): Evaluates 'exp' and discard the result.
    elif isinstance(stmNode, IRT.StatementExpression):
        munch_expression(stmNode.expression)
    # We do not consider the cases for Sequence nodes here, given the modifications
    # done in chapter 8
    elif isinstance(stmNode, IRT.Sequence):
        raise Exception("Found a IRT.Sequence node while munching")
    else:
        raise Exception("No match for IRT node while munching a statement")


def munch_arguments(arg_list: List[IRT.Expression]) -> List[Temp.Temp]:
    temp_list = []
    for argument, register in zip(arg_list, Frame.argument_registers):
        register_temp = Frame.TempMap.register_to_temp[register]
        emit(
            Assembly.Operation(
                line="movq %'s0 %'d0",
                source=[munch_expression(argument)],
                destination=[register_temp],
                jump=[],
            )
        )
        temp_list.append(register_temp)

    for index in range(len(Frame.argument_registers), len(arg_list)):
        emit(
            Assembly.Operation(
                line="pushq %'s0",
                source=[munch_expression(arg_list[index])],
                destination=[],
                jump=[],
            )
        )

    return temp_list


def munch_expression(expNode: IRT.Expression) -> Temp.Temp:
    # BinaryOperation(operator, exp_left, exp_right): Apply the bynary operator
    # 'operator' to operands 'exp_left' and 'exp_right'. 'exp_left' is evaluated
    # before 'exp_right'.
    if isinstance(expNode, IRT.BinaryOperation):
        if isinstance(
            expNode.operator,
            (
                IRT.BinaryOperator.plus,
                IRT.BinaryOperator.minus,
                IRT.BinaryOperator.andOp,
                IRT.BinaryOperator.orOp,
                IRT.BinaryOperator.xor,
            ),
        ):
            # add/sub/and/or/xor src, dst
            temp = Temp.TempManager.new_temp()
            emit(
                Assembly.Move(
                    line="movq %'s0, %'d0",
                    source=[munch_expression(expNode.left)],
                    destination=[temp],
                )
            )
            emit(
                Assembly.Operation(
                    line=f"{binary_operator_to_use[expNode.operator]} %'s1, %'d0",
                    source=[temp, munch_expression(expNode.right)],
                    destination=[temp],
                    jump=[],
                )
            )
            return temp
        elif isinstance(
            expNode.operator, (IRT.BinaryOperator.mul, IRT.BinaryOperator.div)
        ):
            # imul S :  RDX:RAX <--- S * RAX
            # S has the left operand
            # RAX has the right operand
            # RDX:RAX has the result

            # idiv S :  RDX <--- RDX:RAX mod S
            #           RAX <--- RDX:RAX / S
            # S has the divisor
            # RDX:RAX has the dividend
            # RAX has the quotient
            # RDX has the remaining

            temp = Temp.TempManager.new_temp()
            rax = Frame.TempMap.register_to_temp["rax"]
            rdx = Frame.TempMap.register_to_temp["rdx"]

            emit(
                Assembly.Move(
                    line="movq %'s0, %d0'",
                    source=[munch_expression(expNode.left)],
                    destination=[rax],
                )
            )
            emit(
                Assembly.Operation(
                    line="cqto", source=[rax], destination=[rdx], jump=[]
                )
            )
            emit(
                Assembly.Operation(
                    line=f"{binary_operator_to_use[expNode.operator]} %'s2",
                    source=[rax, rdx, munch_expression(expNode.right)],
                    destination=[rax, rdx],
                    jump=[],
                )
            )
            emit(
                Assembly.Move(line="movq %'s0, %'d0", source=[rax], destination=[temp])
            )
            return temp

        elif isinstance(
            expNode.operator,
            (
                IRT.BinaryOperator.lshift,
                IRT.BinaryOperator.rshift,
                IRT.BinaryOperator.arshift,
            ),
        ):
            # sal/sar/shr count, dst
            dst_temp = munch_expression(expNode.right)
            emit(
                Assembly.Operation(
                    line=f"{binary_operator_to_use[expNode.operator]} %'s0, %'d0",
                    source=[munch_expression(expNode.left), dst_temp],
                    destination=[dst_temp],
                    jump=[],
                )
            )
            return dst_temp
        else:
            raise Exception(
                "Munching a node IRT.BinaryOperator with an invalid operator"
            )
    # Memory(addr): The contents of 'WordSize' bytes of memory, starting at address addr.
    elif isinstance(expNode, IRT.Memory):
        temp = Temp.TempManager.new_temp()
        emit(
            Assembly.Move(
                line="movq (%'s0), %'d0",
                source=[munch_expression(expNode.expression)],
                destination=[temp],
            )
        )
        return temp
    # Temporary(temp): he temporary 'temp'.
    elif isinstance(expNode, IRT.Temporary):
        return expNode.temporary
    # Name(n): Symbolic constant 'n' corresponding to an assembly lenguage label
    elif isinstance(expNode, IRT.Name):
        temp = Temp.TempManager.new_temp()
        emit(
            Assembly.Operation(
                line=f"leaq {expNode.Label}(%rip), %'d0",
                source=[],
                destination=[temp],
                jump=[],
            )
        )
        return temp
    # Constant(const): The integer constant 'const'.
    elif isinstance(expNode, IRT.Constant):
        temp = Temp.TempManager.new_temp()
        emit(
            Assembly.Move(
                line=f"movq ${expNode.value}, %'d0",
                source=[],
                destination=[temp],
            )
        )
        return temp
    # Call(function, args): A procedure call: the application of function 'function'
    # to argument list 'args'. The subexpression 'function' is evaluated before the
    # arguments, which are evaluated left to right.
    elif isinstance(expNode, IRT.Call):
        caller_temp = [
            Frame.TempMap.register_to_temp[register]
            for register in Frame.caller_saved_registers
            + Frame.argument_registers
            + ["rax"]
        ]

        emit(
            Assembly.Operation(
                line="call 's0",
                source=[munch_expression(expNode.function)]
                + munch_arguments(expNode.arguments),
                destination=caller_temp,
                jump=[],
            )
        )

        # TODO: hace falta mover el RSP de nuevo? Para mi no, Gianni duda.

        return Frame.TempMap.register_to_temp["rax"]
    # We do not consider the cases for EvaluateSequence nodes here, given the modifications
    # done in chapter 8
    elif isinstance(expNode, IRT.EvaluateSequence):
        raise Exception("Found a IRT.EvaluateSequence node while munching")
    else:
        raise Exception("No match for IRT node while munching an expression")
