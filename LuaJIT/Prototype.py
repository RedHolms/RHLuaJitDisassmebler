from .Types import BytesWritable, BytesInitializable, Serializable
from .Enum import Enum

from .Instruction import Instruction
from .GarbageCollectableConstant import GarbageCollectableConstant
from .ByteStream import ByteStream
from .NumericConstant import NumericConstant
from .NumericConstantsHelper import NumericConstantsHelper

class Prototype: pass
class Bytecode: pass

class PrototypeFlag(Enum):
  HaveChilds  = 0x01
  VarArg      = 0x02
  UsesFFi     = 0x04
  NoJIT       = 0x08
  PatchILOOP  = 0x10

class Prototype(BytesWritable, BytesInitializable, Serializable):
  flags: PrototypeFlag
  parameters_number: int
  frame_size: int
  instructions: list[Instruction]
  upvalues: list[int]
  gc_constants: list[GarbageCollectableConstant]
  nm_constants: list[NumericConstant]
  parent_prototype: Prototype
  child_prototypes: list[Prototype]
  parent_bytecode: Bytecode

  def __init__(self, data: ByteStream = None, parent_bytecode: Bytecode = None) -> None:
    self.flags = 0
    self.parameters_number = 0
    self.frame_size = 0
    self.instructions = []
    self.upvalues = []
    self.gc_constants = []
    self.nm_constants = []
    self.parent_prototype = None
    self.child_prototypes = []
    self.parent_bytecode = parent_bytecode
    
    if data is not None:
      BytesInitializable.__init__(self, data)

  def write(self, output: ByteStream):
    for child in self.child_prototypes:
      child.write(output)

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

    for upvalue in self.upvalues:
      data.write_word(upvalue)
    
    self.gc_constants.reverse()
    for gck in self.gc_constants:
      gck.write(data)
    self.gc_constants.reverse()

    for nmk in self.nm_constants:
      NumericConstantsHelper.write(nmk, data)

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

    for _ in range(gc_constants_count):
      gc_constant = GarbageCollectableConstant()
      gc_constant.parent_prototype = self
      gc_constant.read(input)
      self.gc_constants.append(gc_constant)
    self.gc_constants.reverse()

    for _ in range(nm_constants_count):
      value = NumericConstantsHelper.read(input)
      self.nm_constants.append(value)

    return True

  def serialize(self) -> str:
    result = ""

    have_header = False

    if self.flags & PrototypeFlag.NoJIT:
      result += ".NoJIT\n"
      have_header = True
    if self.flags & PrototypeFlag.PatchILOOP:
      result += ".PatchILOOP\n"
      have_header = True

    index = 0
    for gck in self.gc_constants:
      have_header = True
      result += f".const @{index} = "
      index += 1
      result += gck.serialize()
      result += "\n"
    
    index = 0
    for nmk in self.nm_constants:
      have_header = True
      result += f".number #{index} = {NumericConstantsHelper.serialize(nmk)}\n"
      index += 1

    index = 0
    for upvalue in self.upvalues:
      have_header = True
      result += f".upvalue ^{index} = "

      real_value = upvalue & 0x3FFF
      is_local = (upvalue & 0x8000) != 0
      is_immutable = (upvalue & 0x4000) != 0

      if is_local:
        result += "local "
      if is_immutable:
        result += "readonly "

      result += str(real_value) + "\n"

      index += 1

    if have_header:
      result += "\n"

    for instruction in self.instructions:
      result += instruction.serialize()
      result += "\n"
    result = result[:-1]

    return result