from .Types import IByteStream
from .Utils import normalize_number_sign

def concat_bytes_to_number(data: bytes):
  result = 0
  offset = 0
  for b in data:
    result |= b << offset
    offset += 8
  return result

def transorm_number_to_bytes(number: int, bytes_count: int):
  result = bytearray()
  for i in range(bytes_count):
    result.append((number >> (i*8)) & 0xff)
  return result

class ByteStream(IByteStream):
  data: bytearray
  pointer: int

  def __init__(self, data = None) -> None:
    if data is not None:
      self.data = bytearray(data)
    else:
      self.data = bytearray()
    self.pointer = 0

  def read_bytes(self, number_of_bytes: int) -> bytes:
    value = self.data[self.pointer:self.pointer + number_of_bytes]
    self.pointer += number_of_bytes
    return bytes(value)

  def read_byte(self) -> int:
    return concat_bytes_to_number(self.read_bytes(1))
    
  def read_byte_signed(self) -> int:
    value = concat_bytes_to_number(self.read_bytes(1))
    if value & 0x80:
      return normalize_number_sign(value, 1)
    else:
      return value
    
  def read_word(self) -> int:
    return concat_bytes_to_number(self.read_bytes(2))
  
  def read_word_signed(self) -> int:
    value = concat_bytes_to_number(self.read_bytes(2))
    if value & 0x8000:
      return normalize_number_sign(value, 2)
    else:
      return value
    
  def read_dword(self) -> int:
    return concat_bytes_to_number(self.read_bytes(4))
    
  def read_dword_signed(self) -> int:
    value = concat_bytes_to_number(self.read_bytes(4))
    if value & 0x80000000:
      return normalize_number_sign(value, 4)
    else:
      return value

  def read_uleb128(self) -> int:
    value = self.read_byte()
    if value >= 0x80:
      value &= 0x7f
      offset = 7
      while True:
        new_byte = self.read_byte()
        value |= (new_byte & 0x7f) << offset
        offset += 7
        if new_byte < 0x80:
          break
    return value

  def read_uleb128_signed(self) -> int:
    value = self.read_uleb128()
    if value & 0x80000000:
      return normalize_number_sign(value, 4)
    else:
      return value

  def read_uleb128_33(self) -> tuple[int, bool]:
    value = self.read_byte()
    mark = value & 1
    value >>= 1

    if value >= 0x40:
      value &= 0x3f
      offset = 6
      while True:
        new_byte = self.read_byte()
        value |= (new_byte & 0x7f) << offset
        offset += 7
        if new_byte < 0x80:
          break
    return value, mark

  def read_uleb128_33_signed(self) -> tuple[int, bool]:
    value, mark = self.read_uleb128_33()
    if value & 0x80000000:
      return normalize_number_sign(value, 4), mark
    else:
      return value, mark

  def write_bytes(self, data: bytes):
    for byte in data:
      self.write_byte(byte)

  def write_byte(self, value: int):
    self.data.insert(self.pointer, value)
    self.pointer += 1

  def write_word(self, value: int):
    self.write_bytes(transorm_number_to_bytes(value, 2))

  def write_dword(self, value: int):
    self.write_bytes(transorm_number_to_bytes(value, 4))

  def write_uleb128(self, value: int):
    value &= 0xFFFFFFFF
    while value >= 0x80:
      self.write_byte((value & 0x7f) | 0x80)
      value >>= 7
    self.write_byte(value)

  def write_uleb128_33(self, value: int, mark: bool):
    value &= 0xFFFFFFFF
    if value >= 0x40:
      self.write_byte(((value & 0x3f) << 1) | 0x80 | mark)
      value >>= 6
      self.write_uleb128(value)
    else:
      self.write_byte(((value & 0x3f) << 1) | mark)