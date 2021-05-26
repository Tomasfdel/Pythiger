from temp import Temp, TempLabel, TempManager
from abc import ABC

 # it's a data structure holding:
 # the locations of all the formals
 # instructions required to implement the "view shift"
 # the number of locals allocated so far
 # the label at which the function's machine code is to begin.
class Frame:
  #Creates a new frame for function "name" with "formalEscapes" list of
  #booleans(list of parameters for function "name"). True means
  #escaped variable.
  __init__(self, name: TempLabel, formalEscapes: [bool])
    self.name = name
    # The previous %rbp value is stored at %rbp.
    # Non-volatile registers are stored starting at -8(%rbp).
    self.offset = -8
    # List of "accesses" denoting the locations where
    # the formal parameters will be kept at run time, as seen from
    # inside the callee.
    self.formalParameters = []
    for escape in formalEscapes:
        allocSingleVar(escape)

  # Allocates a new local variable in the frame. The "escape"
  # variable indicates whether the variable escapes or not
  def allocLocal(self, escape: bool) -> InFrame:
      return allocSingleVar(escape)

  def allocSingleVar(self, escape: bool) -> InFrame
    if escape:
        self.offset -= 8
        self.formalParameters.append(InFrame(self.offset))
    else:
        self.formalParameters.append(InRegister(TempManager.new_temp))
    return self.formalParameters[-1]

  # Instruciones requeridas para implementar "cambio de vista"

  # El numero de locales alocados hasta el momento


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
