from .Types import BytesWritable, BytesInitializable, Serializable
from .Enum import Enum
from .Utils import transform_bytes_to_user_string

from .ByteStream import ByteStream

class ConstantTableValueType(Enum):
  NIL = 0
  FALSE = 1
  TRUE = 2
  INT32 = 3
  INT64 = 4
  STRING = 5

class ConstantTableValue(BytesWritable, BytesInitializable, Serializable):
  type: ConstantTableValueType
  value: None | int | bytes

  def __init__(self) -> None:
    self.type = 0
    self.value = None

  def write(self, output: ByteStream):
    type_to_write = self.type
    if type_to_write == ConstantTableValueType.STRING:
      type_to_write += len(self.value)
    
    output.write_uleb128(type_to_write)

    if self.type == ConstantTableValueType.STRING:
      output.write_bytes(self.value)
    elif self.type == ConstantTableValueType.INT32:
      output.write_uleb128(self.value & 0xFFFFFFFF)
    elif self.type == ConstantTableValueType.INT64:
      output.write_uleb128(self.value & 0xFFFFFFFF)
      output.write_uleb128((self.value >> 32) & 0xFFFFFFFF)

  def read(self, input: ByteStream):
    self.type = input.read_uleb128()

    if self.type == ConstantTableValueType.INT32:
      self.value = input.read_uleb128()
    elif self.type == ConstantTableValueType.INT64:
      self.value = input.read_uleb128()
      self.value |= input.read_uleb128() << 32
    elif self.type >= ConstantTableValueType.STRING:
      string_length = self.type - ConstantTableValueType.STRING
      self.type = ConstantTableValueType.STRING
      self.value = input.read_bytes(string_length)
    else:
      self.value = None

  def serialize(self) -> str:
    result = ""

    if self.type == ConstantTableValueType.INT32:
      result += str(self.value)
    elif self.type == ConstantTableValueType.INT64:
      result += str(self.value)
    elif self.type == ConstantTableValueType.NIL:
      result += "nil"
    elif self.type == ConstantTableValueType.FALSE:
      result += "false"
    elif self.type == ConstantTableValueType.TRUE:
      result += "true"
    elif self.type >= ConstantTableValueType.STRING:
      result += f"\"{transform_bytes_to_user_string(self.value)}\""

    return result