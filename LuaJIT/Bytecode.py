from .Types import BytesWritable, BytesInitializable, Serializable

from .ByteStream import ByteStream
from .Prototype import Prototype

class Bytecode(BytesWritable, BytesInitializable, Serializable):
  version: int
  flags: int
  prototypes: list[Prototype]
  prototypes_stack_top: int

  def __init__(self) -> None:
    self.version = 0
    self.flags = 0
    self.prototypes = []
    self.prototypes_stack_top = -1

  def write(self, output: ByteStream):
    output.write_bytes(b"\x1BLJ")
    output.write_byte(self.version)
    output.write_uleb128(self.flags)

    for prototype in self.prototypes:
      prototype.write(output)
    output.write_byte(0)

  def read(self, input: ByteStream):
    header = input.read_bytes(3)
    if header != b"\x1bLJ":
      print(f"invalid header ({header})")
      return

    self.version = input.read_byte()
    self.flags = input.read_uleb128()

    self.prototypes = []
    while True:
      prototype = Prototype()
      prototype.parent_bytecode = self
      if not prototype.read(input):
        break
      self.prototypes_stack_top += 1
      self.prototypes.append(prototype)

  def serialize(self) -> str:
    result = ""

    result += f"; Bytecode version: {self.version}\n"
    result += f"; Bytecode flags: {self.flags}\n"
    
    if self.flags & 2 == 0:
      result += "; Have debug info\n"
    else:
      result += "; No debug info\n"

    if self.flags & 4 == 0:
      result += "; No built-in FFI\n"
    else:
      result += "; Have FFI\n"
    result += "\n"

    index = 0
    for proto in self.prototypes:
      result += f"; Prototype #{index}\n"
      index += 1
      result += proto.serialize()
    result += '\n'

    return result
