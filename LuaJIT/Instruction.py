from .Opcodes import OpcodeInfo, OPCODES_INFO, UNKNOWN_OPCODE_INFO
from .Types import BytesWritable, BytesInitializable, Serializable
from .Utils import get_instruction_argument

from .ByteStream import ByteStream

class Instruction(BytesWritable, BytesInitializable, Serializable):
  opcode: int
  arguments: dict[str, int] # [a/b/c/d] = value

  def __init__(self) -> None:
    self.opcode = 0
    self.arguments = {}

  def get_opcode_info(self) -> OpcodeInfo:
    return OPCODES_INFO[self.opcode] if self.opcode < len(OPCODES_INFO) else UNKNOWN_OPCODE_INFO

  def write(self, output: ByteStream):
    output.write_byte(self.opcode)

    if 'a' in self.arguments:
      output.write_byte(self.arguments['a'])
    else:
      output.write_byte(0)

    if 'd' in self.arguments:
      output.write_word(self.arguments['d'])
    else:
      if 'c' in self.arguments:
        output.write_byte(self.arguments['c'])
      else:
        output.write_byte(0)

      if 'b' in self.arguments:
        output.write_byte(self.arguments['b'])
      else:
        output.write_byte(0)

  def read(self, input: ByteStream):
    value = input.read_dword()

    self.opcode = value & 0xff
    opcode_info = self.get_opcode_info()

    for k, _ in opcode_info.arguments.items():
      self.arguments[k] = get_instruction_argument(value, k)

  def serialize(self) -> str:
    opcode_info = self.get_opcode_info()
    result = opcode_info.name.lower()
    result += (8 - len(opcode_info.name)) * ' '

    prefix = " "
    for k, v in opcode_info.arguments.items():
      result += f"{prefix}{v}:{self.arguments[k]}"
      prefix = ", "

    return result