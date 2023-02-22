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