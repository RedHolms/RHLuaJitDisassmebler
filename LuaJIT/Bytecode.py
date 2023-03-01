from .Types import BytesWritable, BytesInitializable, Serializable
from .Enum import Enum
from .Utils import indent_string

from .ByteStream import ByteStream
from .Prototype import Prototype

class BytecodeFlag(Enum):
  BigEndian       = 0x01
  StripDebugInfo  = 0x02
  UsesFFI         = 0x04
  x64Bit          = 0x08

class Bytecode(BytesWritable, BytesInitializable, Serializable):
  version: int
  flags: BytecodeFlag
  global_chunk: Prototype

  _prototypes_stack: list[Prototype]

  def __init__(self) -> None:
    self.version = 0
    self.flags = 0
    self.global_chunk = None
    self._prototypes_stack = []

  def write(self, output: ByteStream):
    output.write_bytes(b"\x1BLJ")
    output.write_byte(self.version)
    output.write_uleb128(self.flags)

    self.global_chunk.write(output)

    output.write_byte(0)

  def read(self, input: ByteStream):
    header = input.read_bytes(3)
    if header != b"\x1bLJ":
      print(f"invalid header ({header})")
      return

    self.version = input.read_byte()
    self.flags = input.read_uleb128()

    while True:
      prototype = Prototype()
      prototype.parent_bytecode = self
      if not prototype.read(input):
        break
      self._prototypes_stack.append(prototype)
    
    self.global_chunk = self._prototypes_stack[-1]
    self._prototypes_stack.clear()

  def serialize(self) -> str:
    result = ""

    result += f".luajit {self.version if self.version < 0x80 else hex(self.version).capitalize()}\n"
    
    flags = self.flags
    for flag_name, flag in BytecodeFlag:
      if flags & flag:
        result += f".{flag_name}\n"
        # remove this flag
        flags &= ~flag

    if flags != 0:
      # have unknown flags
      offset = 0
      while flags != 0:
        flags >>= 1
        offset += 1

        if not flags & 1:
          continue

        result += f".AddFlag({hex(1 << offset).capitalize()})\n"

    result += "\n"

    result += indent_string("_entry:\n" + self.global_chunk.serialize())

    return result
