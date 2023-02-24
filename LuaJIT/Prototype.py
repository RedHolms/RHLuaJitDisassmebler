from .Types import BytesWritable, BytesInitializable, Serializable

from .Instruction import Instruction
from .GarbageCollectableConstant import GarbageCollectableConstant
from .ByteStream import ByteStream
from .NumericConstant import NumericConstant
from .NumericConstantsHelper import NumericConstantsHelper

class Prototype: pass
class Bytecode: pass

class Prototype(BytesWritable, BytesInitializable, Serializable):
  flags: int
  parameters_number: int
  frame_size: int
  instructions: list[Instruction]
  upvalues: list[int]
  gc_constants: list[GarbageCollectableConstant]
  nm_constants: list[NumericConstant]

  # Values for serializing
  parent_prototype: Prototype
  child_prototypes: list[Prototype]

  # Values for disassembling
  parent_bytecode: Bytecode

  def __init__(self) -> None:
    self.flags = 0
    self.parameters_number = 0
    self.frame_size = 0
    self.instructions = []
    self.upvalues = []
    self.gc_constants = []
    self.nm_constants = []
    self.parent_bytecode = None

  def write(self, output: ByteStream):
    data = ByteStream()
    data.write_byte(self.flags)
    data.write_byte(self.parameters_number)
    data.write_byte(self.frame_size)
    data.write_byte(len(self.upvalues))
    data.write_uleb128(len(self.gc_constants))
    data.write_uleb128(len(self.nm_constants))
    data.write_uleb128(len(self.instructions))
    
    for instruction in self.instructions:
      instruction.write(data)

    self.upvalues.reverse()
    for upvalue in self.upvalues:
      data.write_word(upvalue)
    self.upvalues.reverse()
    
    self.gc_constants.reverse()
    for gck in self.gc_constants:
      gck.write(data)
    self.gc_constants.reverse()

    self.nm_constants.reverse()
    for nmk in self.nm_constants:
      NumericConstantsHelper.write(nmk, data)
    self.nm_constants.reverse()

    output.write_uleb128(len(data.data))
    output.write_bytes(data.data)

  def read(self, input: ByteStream) -> bool:
    assert self.parent_bytecode is not None, "Cannot read Prototype from ByteStream without parent bytecode"

    length_of_prototype = input.read_uleb128()
    if length_of_prototype == 0:
      return False

    self.flags = input.read_byte()
    self.parameters_number = input.read_byte()
    self.frame_size = input.read_byte()
    
    upvalues_count = input.read_byte()
    gc_constants_count = input.read_uleb128()
    nm_constants_count = input.read_uleb128()
    instructions_count = input.read_uleb128()

    for _ in range(instructions_count):
      instruction = Instruction()
      instruction.read(input)
      self.instructions.append(instruction)

    for _ in range(upvalues_count):
      self.upvalues.append(input.read_word())
    self.upvalues.reverse()

    for _ in range(gc_constants_count):
      gc_constant = GarbageCollectableConstant()
      gc_constant.parent_prototype = self
      gc_constant.read(input)
      self.gc_constants.append(gc_constant)
    self.gc_constants.reverse()

    for _ in range(nm_constants_count):
      value = NumericConstantsHelper.read(input)
      self.nm_constants.append(value)
    self.nm_constants.reverse()

    return True

  def serialize(self) -> str:
    result = ""

    result += f"; Prototype flags: {self.flags}\n"

    if self.flags & 1 == 0:
      result += "; No child prototypes\n"
    else:
      result += "; Have child prototypes\n"
    
    if self.flags & 2 != 0:
      result += "; Var-arg function\n"
    
    if self.flags & 4 != 0:
      result += "; Uses BC_KCDATA for FFI datatypes\n"
    
    result += f"; Frame size: {self.frame_size}\n"

    if len(self.gc_constants) == 0:
      result += "; No GC-Constants\n"
    else:
      result += "; GC-Constants:\n"
      index = 0
      for gck in self.gc_constants:
        result += f";   [{index}] = "
        index += 1
        result += gck.serialize()
        result += "\n"
    
    if len(self.nm_constants) == 0:
      result += "; No Numeric Constants\n"
    else:
      result += "; Numeric Constants:\n"
      index = 0
      for nmk in self.nm_constants:
        result += f";   [{index}] = {NumericConstantsHelper.serialize(nmk)}\n"
        index += 1

    if len(self.upvalues) == 0:
      result += "; No upvalues\n"
    else:
      result += "; Upvalues:\n"
      index = 0
      for upvalue in self.upvalues:
        result += f";   [{index}] = {upvalue}\n"
        index += 1

    result += "; Bytecode:\n\n"

    address = 0
    for instruction in self.instructions:
      result += f"{'%04d' % address}  "
      result += instruction.serialize()
      result += "\n"
      address += 1
    
    result += "\n"

    return result