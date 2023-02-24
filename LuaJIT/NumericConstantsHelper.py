from .Utils import normalize_number_sign, interpret_float_as_int, interpret_int_as_float

from .ByteStream import ByteStream
from .NumericConstant import NumericConstant

class NumericConstantsHelper:
  @staticmethod
  def serialize(numeric_constant: NumericConstant) -> str:
    return str(numeric_constant)

  @staticmethod
  def write(numeric_constant: NumericConstant, output: ByteStream):
    if type(numeric_constant) == int:
      output.write_uleb128_33(numeric_constant, False)
    else:
      # assert type(numeric_constant) == float
      to_write = interpret_float_as_int(numeric_constant)
      output.write_uleb128_33(to_write & 0xFFFFFFFF, True)
      output.write_uleb128(to_write >> 32)

  @staticmethod
  def read(input: ByteStream) -> NumericConstant:
    first, is_float = input.read_uleb128_33()
    if is_float:
      second = input.read_uleb128()
      int_value = first | (second << 32)
      return interpret_int_as_float(int_value)
    else:
      return normalize_number_sign(first, 4)