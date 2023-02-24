import numpy

def transform_bytes_to_user_string(data: bytes):
  try:
    return data.decode("utf-8")
  except: pass

  try:
    return data.decode("cp1251")
  except: pass

  return str(data)[2:-1]

def get_instruction_argument(instruction: int, argument_name: str) -> int:
  match argument_name:
    case 'a':
      return (instruction >> 8) & 0xff
    case 'b':
      return (instruction >> 24) & 0xff
    case 'c':
      return (instruction >> 16) & 0xff
    case 'd':
      return (instruction >> 16) & 0xffff
  return None

def normalize_number_sign(value: int, size_in_bytes: int) -> int:
  sign_mask = 1 << ((size_in_bytes * 8) - 1)
  if value & sign_mask:
    return (-1 & ~((1 << (size_in_bytes * 8)) - 1)) | value
  else:
    return value

def interpret_int_as_float(int_value: int) -> float:
  return numpy.array([ int_value ], dtype="uint64").view(dtype="double")[0]

def interpret_float_as_int(float_value: float) -> int:
  return numpy.array([ float_value ], dtype="double").view(dtype="uint64")[0]