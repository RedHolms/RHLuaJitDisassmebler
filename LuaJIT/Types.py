from abc import abstractclassmethod

# Interface to bytestream-like object
class IByteStream:
  data: bytearray
  pointer: int

  # If data specified, initializes bytestream with bytes-like object.
  # Otherwise, initializes bytestream with empty bytes
  @abstractclassmethod
  def __init__(self, data = None) -> None:
    pass

  # Read specified number of bytes from bytestream
  @abstractclassmethod
  def read_bytes(self, number_of_bytes: int) -> bytes:
    pass

  # Read single byte
  @abstractclassmethod
  def read_byte(self) -> int:
    pass
  
  # Read single word (two bytes)
  @abstractclassmethod
  def read_word(self) -> int:
    pass
    
  # Read single dword (four bytes)
  @abstractclassmethod
  def read_dword(self) -> int:
    pass

  # Read uleb128-encoded dword
  @abstractclassmethod
  def read_uleb128(self) -> int:
    pass
  
  # Read uleb128-encoded dword with mark
  @abstractclassmethod
  def read_uleb128_33(self) -> tuple[int, bool]:
    pass

  # Write bytes-like object to bytestream
  @abstractclassmethod
  def write_bytes(self, data: bytes):
    pass

  # Write single byte
  @abstractclassmethod
  def write_byte(self, value: int):
    pass

  # Write single word (two bytes)
  @abstractclassmethod
  def write_word(self, value: int):
    pass
  
  # Write single dword (four bytes)
  @abstractclassmethod
  def write_dword(self, value: int):
    pass

  # Encode dword as uleb128
  @abstractclassmethod
  def write_uleb128(self, value: int):
    pass

  # Encode dword as uleb128 with mark
  @abstractclassmethod
  def write_uleb128_33(self, value: int, mark: bool):
    pass

# Object that can be serialized to user-friendly string
class Serializable:
  @abstractclassmethod
  def serialize(self) -> str:
    pass

# Object that can be initialized (using read() method!) from bytestream-like object
class BytesInitializable:
  @abstractclassmethod
  def read(self, input: IByteStream):
    pass

# Object that can be writed to bytestream-like object
class BytesWritable:
  @abstractclassmethod
  def write(self, output: IByteStream):
    pass