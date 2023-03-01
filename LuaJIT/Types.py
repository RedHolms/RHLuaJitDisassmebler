from abc import abstractmethod as AbstractMethod, ABC as AbstractClass

# Interface to bytestream-like object
class IByteStream(AbstractClass):
  data: bytearray # Raw data
  pointer: int # Pointer (index) where functions will read or write data

  # If data specified, initializes bytestream with bytes-like object.
  # Otherwise, initializes bytestream with empty bytes
  @AbstractMethod
  def __init__(self, data = None) -> None:
    pass

  # Read specified number of bytes from bytestream
  @AbstractMethod
  def read_bytes(self, number_of_bytes: int) -> bytes:
    pass

  # Read single byte
  @AbstractMethod
  def read_byte(self) -> int:
    pass
  
  # Read single word (two bytes)
  @AbstractMethod
  def read_word(self) -> int:
    pass
    
  # Read single dword (four bytes)
  @AbstractMethod
  def read_dword(self) -> int:
    pass

  # Read uleb128-encoded dword
  @AbstractMethod
  def read_uleb128(self) -> int:
    pass
  
  # Read uleb128-encoded dword with mark
  @AbstractMethod
  def read_uleb128_33(self) -> tuple[int, bool]:
    pass

  # Write bytes-like object to bytestream
  @AbstractMethod
  def write_bytes(self, data: bytes):
    pass

  # Write single byte
  @AbstractMethod
  def write_byte(self, value: int):
    pass

  # Write single word (two bytes)
  @AbstractMethod
  def write_word(self, value: int):
    pass
  
  # Write single dword (four bytes)
  @AbstractMethod
  def write_dword(self, value: int):
    pass

  # Encode dword as uleb128
  @AbstractMethod
  def write_uleb128(self, value: int):
    pass

  # Encode dword as uleb128 with mark
  @AbstractMethod
  def write_uleb128_33(self, value: int, mark: bool):
    pass

# Object that can be serialized to user-friendly string
class Serializable(AbstractClass):
  @AbstractMethod
  def serialize(self) -> str:
    pass

# Object that can be initialized (using read() method!) from bytestream-like object
class BytesInitializable(AbstractClass):
  @AbstractMethod
  def read(self, input: IByteStream):
    pass

# Object that can be writed to bytestream-like object
class BytesWritable(AbstractClass):
  @AbstractMethod
  def write(self, output: IByteStream):
    pass