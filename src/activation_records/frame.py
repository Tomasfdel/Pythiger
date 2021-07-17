from typing import List, Dict

from dataclasses import dataclass

from abc import ABC
from activation_records.temp import Temp, TempLabel, TempManager
import intermediate_representation.tree as IRT
import instruction_selection.assembly as Assembly

# Constant for the machine's word size.
word_size = 8

# The register lists should not overlap according to Appel, but some are
# ambiguous (like rbp, which is "special" but also callee-saved).
# The assignment to each list has been done in accordance to:
# https://web.stanford.edu/class/archive/cs/cs107/cs107.1216/resources/x86-64-reference.pdf

# A list of registers used to implement "special" registers.
special_registers = ["rip", "rsp", "rax"]

# A list of registers in which to pass outgoing arguments
# (including the static link).
argument_registers = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]

# A list of registers that the called procedure (callee) must preserve
# unchanged (or save and restore).
callee_saved_registers = ["rbx", "rbp", "r12", "r13", "r14", "r15"]

# A list of registers that the callee may trash.
caller_saved_registers = ["r10", "r11"]

all_registers = (
    special_registers
    + argument_registers
    + callee_saved_registers
    + caller_saved_registers
)


# Bidirectional mapping between registers and temporaries.
class TempMap:
    # Dictionary mapping registers to temporaries.
    register_to_temp = {}
    # Dictionary mapping temporaries to registers.
    temp_to_register = {}

    @classmethod
    def initialize(cls):
        for register in all_registers:
            temp = TempManager.new_temp()
            cls.register_to_temp[register] = temp
            cls.temp_to_register[temp] = register

    @classmethod
    def update_temp_to_register(cls, register_allocation: Dict[Temp, Temp]):
        for temporary in register_allocation:
            cls.temp_to_register[temporary] = cls.temp_to_register[
                register_allocation[temporary]
            ]


# Temporal corresponding to the frame pointer register rbp.
def frame_pointer() -> Temp:
    return TempMap.register_to_temp["rbp"]


# Temporal corresponding to the return value register rax.
def return_value() -> Temp:
    return TempMap.register_to_temp["rax"]


# TODO: Placeholder for testing.
def temp_to_str(temp: Temp) -> str:
    register = TempMap.temp_to_register.get(temp)
    if register:
        return register

    return f"t{temp}"


# Access describes formals and locals stored in a frame or in registers
# as seen from the calee's perspective.
class Access(ABC):
    pass


# InFrame(X) indicates a memory location at offset X from the frame pointer.
@dataclass
class InFrame(Access):
    offset: int


# InReg(t84) indicates storage in the "register" t84.
@dataclass
class InRegister(Access):
    register: Temp


# Frame is the class responsible for:
# * the locations of all the formals.
# * instructions required to implement the "view shift".
# * the number of locals allocated so far.
# * the label at which the function's machine code is to begin.
class Frame:
    # Creates a new frame for function "name" with "formalEscapes" list of
    # booleans (list of parameters for function "name"). True means
    # escaped variable.
    def __init__(self, name: TempLabel, formal_escapes: List[bool]):
        self.name = name
        # The previous %rbp value is stored at 0(%rbp).
        # Non-volatile registers are stored starting at -8(%rbp).
        # (subtraction is performed before allocation)
        self.offset = 0

        # [Access] denoting the locations where the formal parameters will be
        # kept at run time, as seen from inside the callee.
        self.formal_parameters = []
        # [Access] denoting the locations where the local variables will be
        # kept at run time, as seen from inside the callee.
        self.local_variables = []
        for escape in formal_escapes:
            self._alloc_single_var(escape, self.formal_parameters)

    # Allocates a new local variable in the frame. The "escape"
    # variable indicates whether the variable escapes or not.
    def alloc_local(self, escape: bool) -> Access:
        return self._alloc_single_var(escape, self.local_variables)

    # Allocates a single variable or parameter in the frame and adds it
    # to access_list.
    def _alloc_single_var(self, escape: bool, access_list: List[Access]) -> Access:
        if escape:
            self.offset -= word_size
            access_list.append(InFrame(self.offset))
        else:
            access_list.append(InRegister(TempManager.new_temp()))
        return access_list[-1]

    # Instructions required for "view shift".272

    # Number of allocated locals so far.
    # TODO: Where is this function needed?
    def allocated_locals_count(self):
        return len(self.local_variables)


# This function is used by Translate to turn a Frame.Access into an IRT.Expression.
# The frame_pointer argument is the address of the stack frame that the access lives in.
# If access is a register access, such as InReg(t82), then the frame_pointer argument
# will be discarded.
def access_to_exp(access: Access, frame_pointer: IRT.Expression) -> IRT.Expression:
    if isinstance(access, InFrame):
        return IRT.Memory(
            IRT.BinaryOperation(
                IRT.BinaryOperator.plus, frame_pointer, IRT.Constant(access.offset)
            )
        )
    if isinstance(access, InRegister):
        return IRT.Temporary(access.register)


# Sometimes we will need to call external functions that as written in C or assembly language
# (such as a function that allocates memory for a Tiger array).
# However, sometimes the C compiler puts an underscore at the beginning of each label, or
# the calling convention for C functions may differ from those of Tiger functions. All these target
# machine specific details should be encapsulated in this function, which creates a Tree expression
# that creates the relevant function call. The simplest form for this function would be something
# like return T_Call(T_Name(Temp_namedlabel(s)), args); , but it may have to be adapted for
# static links, underscores in labels, and so on.
# TODO: See what shape this expression should have once we move to define the runtime functions.
def external_call(
    function_name: str, arguments: List[IRT.Expression]
) -> IRT.Expression:
    return IRT.Call(IRT.Name(TempManager.named_label(function_name)), arguments)


# This applies the view shift of calling a function.
# This means concatenating a sequence of IRT.Moves to the function body, where each move changes
# a register parameter to the place from which it is seen from within the function.
def shift_view(frame: Frame, function_body: IRT.Statement) -> IRT.Statement:
    shift_parameters = []
    for access, argument_register in zip(frame.formal_parameters, argument_registers):
        # TODO: Cuando tengamos variables que no escapan, aca va un if para
        # ver si el access es InRegister o InFrame.
        shift_parameters.append(
            IRT.Move(
                IRT.Memory(
                    IRT.BinaryOperation(
                        IRT.BinaryOperator.plus,
                        IRT.Temporary(frame_pointer()),
                        IRT.Constant(access.offset),
                    )
                ),
                IRT.Temporary(TempMap.register_to_temp[argument_register]),
            )
        )

    return IRT.Sequence(shift_parameters + [function_body])


# This preserves the callee_saved registers across a function call.
# We need to make up new temporaries for each callee-save register. On entry, we move
# all these registers to their new temporary locations, and on exit, we move them back.
def preserve_callee_registers(
    frame: Frame, function_body: IRT.Statement
) -> IRT.Statement:
    save_registers = []
    restore_registers = []
    for callee_register in callee_saved_registers:
        temp = TempManager.new_temp()
        save_registers.append(
            IRT.Move(
                IRT.Temporary(temp),
                IRT.Temporary(TempMap.register_to_temp[callee_register]),
            )
        )
        restore_registers.append(
            IRT.Move(
                IRT.Temporary(TempMap.register_to_temp[callee_register]),
                IRT.Temporary(temp),
            )
        )
    return IRT.Sequence(save_registers + [function_body] + restore_registers)


# This function appends a “sink” instruction to the function body to tell the
# register allocator that certain registers are live at procedure exit.
def sink(function_body: List[Assembly.Instruction]) -> List[Assembly.Instruction]:
    # TODO: Check if rax needs to be in this list.
    sink_registers = callee_saved_registers + ["rsp"]
    sink_temps = [TempMap.register_to_temp[register] for register in sink_registers]
    function_body.append(Assembly.Operation(line="", src=sink_temps, dst=[], jump=None))
    return function_body


# TODO: Find a better name.
def proc_entry_exit3(
    frame: Frame, body: List[Assembly.Instruction]
) -> Assembly.Procedure:
    # TODO: This is a scaffold version, as Appel calls it.
    # It will be implemented for real in page 269 (niCe book).
    return Assembly.Procedure(
        prologue=f"PROCEDURE {frame.name}\n", body=body, epilogue=f"END {frame.name}\n"
    )
