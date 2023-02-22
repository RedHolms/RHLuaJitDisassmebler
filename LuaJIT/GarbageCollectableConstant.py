from .Types import BytesWritable, BytesInitializable, Serializable
from .Enum import Enum
from .Utils import transform_bytes_to_user_string

from .ConstantTable import ConstantTable
from .ByteStream import ByteStream

class GarbageCollectableConstantType(Enum):
  CHILD = 0
  TABLE = 1
  INT64 = 2
  UINT64 = 3
  COMPLEX = 4
  STRING = 5

class GarbageCollectableConstant(BytesWritable, BytesInitializable, Serializable):
  type: GarbageCollectableConstantType
  value: ConstantTable | int | complex | bytes

  parent_prototype: any

  def __init__(self) -> None:
    self.type = 0
    self.value = None
    self.parent_prototype = None

  def write(self, output: ByteStream):
    type_to_write = self.type
    if type_to_write == GarbageCollectableConstantType.STRING:
      type_to_write += len(self.value)
    
    output.write_uleb128(type_to_write)

    if self.type == GarbageCollectableConstantType.TABLE:
      self.value.write(output)
    elif self.type == GarbageCollectableConstantType.INT64 or self.type == GarbageCollectableConstantType.UINT64:
      output.write_uleb128(self.value & 0xFFFFFFFF)
      output.write_uleb128((self.value >> 32) & 0xFFFFFFFF)
    elif self.type == GarbageCollectableConstantType.COMPLEX:
      output.write_uleb128(self.value.real & 0xFFFFFFFF)
      output.write_uleb128((self.value.real >> 32) & 0xFFFFFFFF)
      output.write_uleb128(self.value.imag & 0xFFFFFFFF)
      output.write_uleb128((self.value.imag >> 32) & 0xFFFFFFFF)
    elif self.type == GarbageCollectableConstantType.STRING:
      output.write_bytes(self.value)

  def read(self, input: ByteStream):
    assert self.parent_prototype is not None, "Cannot read GarbageCollectableConstant from ByteStream without parent prototype"
    assert self.parent_prototype.parent_bytecode is not None, "Cannot read GarbageCollectableConstant from ByteStream without parent bytecode"
    
    parent_bytecode = self.parent_prototype.parent_bytecode

    self.type = input.read_uleb128()
    
    if self.type == GarbageCollectableConstantType.CHILD:
      self.value = parent_bytecode.prototypes_stack_top
      parent_bytecode.prototypes_stack_top -= 1
    elif self.type == GarbageCollectableConstantType.TABLE:
      table = ConstantTable()
      table.read(input)
      self.value = table
    elif self.type == GarbageCollectableConstantType.INT64 or self.type == GarbageCollectableConstantType.UINT64:
      self.value = input.read_uleb128()
      self.value |= input.read_uleb128() << 32
    elif self.type == GarbageCollectableConstantType.COMPLEX:
      real = input.read_uleb128()
      real |= input.read_uleb128() << 32
      imag = input.read_uleb128()
      imag |= input.read_uleb128() << 32
      self.value = complex(real, imag)
    elif self.type >= GarbageCollectableConstantType.STRING:
      string_length = self.type - GarbageCollectableConstantType.STRING
      self.type = GarbageCollectableConstantType.STRING
      self.value = input.read_bytes(string_length)

  def serialize(self) -> str:
    result = ""

    if self.type == GarbageCollectableConstantType.CHILD:
      result += "Prototype#" + str(self.value)
    elif self.type == GarbageCollectableConstantType.TABLE:
      result += self.value.serialize()
    elif self.type == GarbageCollectableConstantType.INT64 or self.type == GarbageCollectableConstantType.UINT64:
      result += str(self.value) + ("LL" if self.type == GarbageCollectableConstantType.INT64 else "ULL")
    elif self.type == GarbageCollectableConstantType.COMPLEX:
      result += f"{self.value.real}+{self.value.imag}i"
    elif self.type >= GarbageCollectableConstantType.STRING:
      result += f"\"{transform_bytes_to_user_string(self.value)}\""

    return result