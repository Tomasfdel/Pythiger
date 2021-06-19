import intermediate_representation.tree as IRT
import assembly as Assembly
import activation_records.temp as Temp

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

# TODO: Add exceptions.
# TODO: change assembly operations to match 64 bit use


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
# TODO: There are two operators for multiplication and division, one for
# signed values and another for unsigned ones. Which one should we use, if not both?
# Currently using signed version of mul and div.
binary_operator_to_use = {
    IRT.BinaryOperator.plus: "add",
    IRT.BinaryOperator.minus: "sub",
    IRT.BinaryOperator.mul: "imul",
    IRT.BinaryOperator.div: "idiv",
    IRT.BinaryOperator.andOp: "and",
    IRT.BinaryOperator.orOp: "or",
    IRT.BinaryOperator.lshift: "sal",
    IRT.BinaryOperator.rshift: "sar",
    IRT.BinaryOperator.arshift: "shr",
    IRT.BinaryOperator.xor: "xor",
}


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
                line="cmp %'s0, %'s1",
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

    if isinstance(stmNode, IRT.Move):
        # Warning: the IRT is built using the syntax as (move dst, src).
        # Here we swap the order of the expressions to match the AT&T syntax (move src, dst)
        # Move(Temp t, e)
        if isinstance(stmNode.temporary, IRT.Temporary):
            emit(
                Assembly.Move(
                    line="movq %'s0, %'d0",
                    source=[munchExp(stmNode.expression)],
                    destination=[munchExp(stmNode.temporary)],
                )
            )
        elif isinstance(stmNode.temporary, IRT.Memory):
            # TODO: Triple check that this Assembly operation is actually a Move
            # Move(mem(e1), e2): evaluate e1, yielding address addr.
            # Then evaluate e2 and store the result in memory starting at addr
            emit(
                Assembly.Move(
                    line="movq %'s0, (%'s1)",
                    source=[
                        munchExp(stmNode.expression),
                        munchExp(stmNode.temporary.expression),
                    ],
                    destination=[],
                )
            )
        else:
            # TODO: Throw exception error "No match for node IRT.Move"
            pass

    if isinstance(stmNode, IRT.StatementExpression):
        munchExp(stmNode.expression)

    else:
        # TODO: Throw exception error "No match for the IRT node in statement"
        pass


def munchExp(expNode: IRT.Expression) -> Temp.Temp:
    if isinstance(expNode, IRT.BinaryOperation):
        if isinstance(
            expNode.operator, (IRT.BinaryOperator.plus, IRT.BinaryOperator.minus)
        ):
            # add/sub src, dst
            temp = Temp.TempManager.new_temp()
            emit(
                Assembly.Move(
                    line="mov %'s0, %'d0",
                    source=[munchExp(expNode.left)],
                    destination=[temp],
                )
            )
            emit(
                Assembly.Operation(
                    line=f"{binary_operator_to_use[expNode.operator]} %'s1, %'d0",
                    source=[temp, munchExp(expNode.right)],
                    destination=[temp],
                    jump=[],
                )
            )
            return temp
        elif isinstance(
            expNode.operator, (IRT.BinaryOperator.mul, IRT.BinaryOperator.div)
        ):
            # imul/idiv src, dst
            # TODO: complete this case
            pass
        elif isinstance(
            expNode.operator,
            (IRT.BinaryOperator.andOp, IRT.BinaryOperator.orOp, IRT.BinaryOperator.xor),
        ):
            # and/or/xor src, dst
            # TODO: add to previous case as to not repeat code.
            temp = Temp.TempManager.new_temp()
            emit(
                Assembly.Move(
                    line="mov %'s0, %'d0",
                    source=[munchExp(expNode.left)],
                    destination=[temp],
                )
            )
            emit(
                Assembly.Operation(
                    line=f"{binary_operator_to_use[expNode.operator]} %'s1, %'d0",
                    source=[temp, munchExp(expNode.right)],
                    destination=[temp],
                    jump=[],
                )
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
            dst_temp = munchExp(expNode.right)
            emit(
                Assembly.Operation(
                    line=f"{binary_operator_to_use[expNode.operator]} %'s0, %'d0",
                    source=[munchExp(expNode.left), dst_temp],
                    destination=[dst_temp],
                    jump=[],
                )
            )
            return dst_temp
        else:
            # TODO: Throw exception error "Not a valid operator"
            pass

    # Mem(e): contenido en WordSize Bytes que está en la dirección 'e'
    elif isinstance(expNode, IRT.Memory):
        temp = Temp.TempManager.new_temp()
        emit(
            Assembly.Move(
                line="mov (%'s0), %'d0",
                source=[munchExp(expNode.expression)],
                destination=[temp],
            )
        )
        return temp

    elif isinstance(expNode, IRT.Temporary):
        return expNode.temporary

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

    elif isinstance(expNode, IRT.Call):
        # Lo que deberíamos hacer:
        # pushear caller saved arguments
        # hacer el call (line="call expNode.function")
        # popear caller saved arguments
        # function = munchExp(expNode.function)
        # arguments = [munchExp(argument) for argument in expNode.arguments]
        # emit("CALL")
        # munchExp(expNode.function)
        # for argument in expNode.arguments:
        #     munchExp(argument)
        pass

    # TODO: Ask tomasu what this is.
    elif isinstance(expNode, IRT.Condition):
        # emit("CONDITION")
        # munchStm(statement)
        pass
    else:
        # Throw exception error "No match for the IRT node in expression"
        pass
