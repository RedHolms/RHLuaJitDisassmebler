import sys

from LuaJIT.Bytecode import Bytecode
from LuaJIT.ByteStream import ByteStream

def main():
  if len(sys.argv) < 2:
    print("No input file")
    return 1

  input_file_name = sys.argv[1]
  output_file_name = None

  if len(sys.argv) < 3:
    output_file_name = input_file_name + ".luas"
  else:
    output_file_name = sys.argv[3]

  file_content = None
  with open(input_file_name, "rb") as f:
    file_content = ByteStream(f.read())
    f.close()

  bytecode = Bytecode()
  bytecode.read(file_content)

  with open(output_file_name, "w+", encoding="utf-8") as f:
    f.write(bytecode.serialize())
    f.close()

  return 0

if __name__ == "__main__":
  exit(main())