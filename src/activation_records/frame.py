from typing import List

from dataclasses import dataclass

from intermediate_representation.translated_expression import Expression
from intermediate_representation.tree import Statement
from temp import Temp, TempLabel, TempManager
from abc import ABC


# La clase Access describe formals y locals que están en frame
# o en registros. Esto es un tipo de dato abstracto, por lo que el
# contenido es visible solamente en la clase Frame.
# Fijate si podes poner Access solo total el modulo te maskea los
# nombres.
class FrameAccess(ABC):
    pass


# InFrame(X) indica una ubicación de memoria en el offset X respecto
# al frame pointer, es decir, %rbp.
@dataclass
class InFrame(FrameAccess):
    offset: int


# InReg(t84) indica que se va a mantener en el "registro" t84.
@dataclass
class InRegister(FrameAccess):
    register: Temp


# it's a data structure holding:
# the locations of all the formals
# instructions required to implement the "view shift"
# the number of locals allocated so far
# the label at which the function's machine code is to begin.
class Frame:
    # Creates a new frame for function "name" with "formalEscapes" list of
    # booleans(list of parameters for function "name"). True means
    # escaped variable.
    def __init__(self, name: TempLabel, formal_escapes: [bool]):
        self.name = name
        # The previous %rbp value is stored at %rbp.
        # Non-volatile registers are stored starting at -8(%rbp).
        self.offset = -8
        # List of "accesses" denoting the locations where
        # the formal parameters will be kept at run time, as seen from
        # inside the callee.
        self.formalParameters = []
        for escape in formal_escapes:
            self.alloc_single_var(escape)

    # Allocates a new local variable in the frame. The "escape"
    # variable indicates whether the variable escapes or not
    def alloc_local(self, escape: bool) -> InFrame:
        return self.alloc_single_var(escape)

    def alloc_single_var(self, escape: bool) -> InFrame:
        if escape:
            self.offset -= 8
            self.formalParameters.append(InFrame(self.offset))
        else:
            self.formalParameters.append(InRegister(TempManager.new_temp()))
        return self.formalParameters[-1]

    # Instruciones requeridas para implementar "cambio de vista"

    # El numero de locales alocados hasta el momento


# Extra definitions found on Chapter 7. Feel free to rename them as you consider.

# Frame pointer register FP.
# F_FP: Temp

# Constant for the machine's word size.
# F_wordSize: int


# This function is used by Translate to turn a Frame_access into an intermediate representation
# Tree expression. The Tree_exp argument is the address of the stack frame that the access lives in.
# If acc is a register access, such as InReg(t82), then the frame address argument will be discarded
# and the result will be simply Temp(t82).
def frame_exp(access: FrameAccess, frame_ptr: Expression) -> Expression:
    pass


# Sometimes we will need to call external functions that as written in C or assembly language
# (such as a function that allocates memory for a Tiger array).
# However, sometimes the C compiler puts an underscore at the beginning of each label, or the
# calling convention for C functions may differ from those of Tiger functions. All these target
# machine specific details should be encapsulated in this function, which creates a Tree expression
# that creates the relevant function call. The simplest form for this function would be something
# like return T_Call(T_Name(Temp_namedlabel(s)), args); ,
# but it may have to be adapted for static links, underscores in labels, and so on.
def external_call(function_name: str, arguments: List[Expression]) -> Expression:
    pass


# Location of a function's return value (RV) as specified by the machine-specific frame structure.
# F_RV: Temp


# This applies the view shift of calling a function, which is explained in Chapter 6.
# Looks like this method is explained later, so we can use a dummy implementation
# that just returns stm for now.
def F_procEntryExit1(frame: Frame, statement: Statement) -> Statement:
    return statement


class Fragment(ABC):
    pass


@dataclass
class StringFragment(Fragment):
    label: TempLabel
    string: str


@dataclass
class ProcessFragment(Fragment):
    body: Statement
    frame: Frame
