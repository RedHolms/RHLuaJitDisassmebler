from .Types import BytesWritable, BytesInitializable, Serializable

from .ByteStream import ByteStream
from .ConstantTableValue import ConstantTableValue

class ConstantTable(BytesWritable, BytesInitializable, Serializable):
  array: list[ConstantTableValue]
  hash: list[tuple[ConstantTableValue, ConstantTableValue]]

  def __init__(self) -> None:
    self.array = []
    self.hash = []

  def write(self, output: ByteStream):
    output.write_uleb128(len(self.array))
    output.write_uleb128(len(self.hash))

    for value in self.array:
      value.write(output)
    
    for key, value in self.hash:
      key.write(output)
      value.write(output)

  def read(self, input: ByteStream):
    array_count = input.read_uleb128()
    hash_count = input.read_uleb128()

    for _ in range(array_count):
      value = ConstantTableValue()
      value.read(input)
      self.array.append(value)
    
    for _ in range(hash_count):
      key = ConstantTableValue()
      key.read(input)
      value = ConstantTableValue()
      value.read(input)
      self.hash.append((key, value))

  def serialize(self) -> str:
    result = ""

    if len(self.array) == 0 and len(self.hash) == 0:
      result += "{}"
      return result
    
    result += "{\n"

    index = 0
    for value in self.array:
      result += f"  [{index}] = "
      index += 1
      result += value.serialize()
      result += "\n"

    for key, value in self.hash:
      result += "  ["
      result += key.serialize()
      result += "] = "
      result += value.serialize()
      result += "\n"

    result += "}"

    return result