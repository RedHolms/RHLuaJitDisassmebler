class OpcodeInfo:
  name: str
  arguments: dict[str, str] # Maps: [argument name (a, b, c or d)] = argument type

  def __init__(self, name, a = None, b = None, c = None, d = None):
    self.name = name
    self.arguments = {}

    if a is not None:
      self.arguments['a'] = a
    if b is not None:
      self.arguments['b'] = b
    if c is not None:
      self.arguments['c'] = c
    if d is not None:
      self.arguments['d'] = d

OPCODES_INFO = [
  OpcodeInfo("ISLT", a="var", d="var"),
  OpcodeInfo("ISGE", a="var", d="var"),
  OpcodeInfo("ISLE", a="var", d="var"),
  OpcodeInfo("ISGT", a="var", d="var"),
  OpcodeInfo("ISEQV", a="var", d="var"),
  OpcodeInfo("ISNEV", a="var", d="var"),
  OpcodeInfo("ISEQS", a="var", d="str"),
  OpcodeInfo("ISNES", a="var", d="str"),
  OpcodeInfo("ISEQN", a="var", d="num"),
  OpcodeInfo("ISNEN", a="var", d="num"),
  OpcodeInfo("ISEQP", a="var", d="pri"),
  OpcodeInfo("ISNEP", a="var", d="pri"),

  # Unary test and copy ops.
  OpcodeInfo("ISTC", a="dst", d="var"),
  OpcodeInfo("ISFC", a="dst", d="var"),
  OpcodeInfo("IST", d="var"),
  OpcodeInfo("ISF", d="var"),

  # WARNING: 2nd version only
  OpcodeInfo("ISTYPE", a="var", d="lit"),
  OpcodeInfo("ISNUM", a="var", d="lit"),

  # Unary ops.
  OpcodeInfo("MOV", a="dst", d="var"),
  OpcodeInfo("NOT", a="dst", d="var"),
  OpcodeInfo("UNM", a="dst", d="var"),
  OpcodeInfo("LEN", a="dst", d="var"),

  # Binary ops. ORDER OPR. VV last, POW must be next.
  OpcodeInfo("ADDVN", a="dst", b="var", c="num"),
  OpcodeInfo("SUBVN", a="dst", b="var", c="num"),
  OpcodeInfo("MULVN", a="dst", b="var", c="num"),
  OpcodeInfo("DIVVN", a="dst", b="var", c="num"),
  OpcodeInfo("MODVN", a="dst", b="var", c="num"),
  OpcodeInfo("ADDNV", a="dst", b="var", c="num"),
  OpcodeInfo("SUBNV", a="dst", b="var", c="num"),
  OpcodeInfo("MULNV", a="dst", b="var", c="num"),
  OpcodeInfo("DIVNV", a="dst", b="var", c="num"),
  OpcodeInfo("MODNV", a="dst", b="var", c="num"),
  OpcodeInfo("ADDVV", a="dst", b="var", c="var"),
  OpcodeInfo("SUBVV", a="dst", b="var", c="var"),
  OpcodeInfo("MULVV", a="dst", b="var", c="var"),
  OpcodeInfo("DIVVV", a="dst", b="var", c="var"),
  OpcodeInfo("MODVV", a="dst", b="var", c="var"),
  OpcodeInfo("POW", a="dst", b="var", c="var"),
  OpcodeInfo("CAT", a="dst", b="rbase", c="rbase"),

  # Constant ops.
  OpcodeInfo("KSTR", a="dst", d="str"),
  OpcodeInfo("KCDATA", a="dst", d="cdata"),
  OpcodeInfo("KSHORT", a="dst", d="lits"),
  OpcodeInfo("KNUM", a="dst", d="num"),
  OpcodeInfo("KPRI", a="dst", d="pri"),
  OpcodeInfo("KNIL", a="base", d="base"),

  # Upvalue and function ops.
  OpcodeInfo("UGET", a="dst", d="uv"),
  OpcodeInfo("USETV", a="uv", d="var"),
  OpcodeInfo("USETS", a="uv", d="str"),
  OpcodeInfo("USETN", a="uv", d="num"),
  OpcodeInfo("USETP", a="uv", d="pri"),
  OpcodeInfo("UCLO", a="rbase", d="jump"),
  OpcodeInfo("FNEW", a="dst", d="func"),

  # Table ops.
  OpcodeInfo("TNEW", a="dst", d="lit"),
  OpcodeInfo("TDUP", a="dst", d="tab"),
  OpcodeInfo("GGET", a="dst", d="str"),
  OpcodeInfo("GSET", a="var", d="str"),
  OpcodeInfo("TGETV", a="dst", b="var", c="var"),
  OpcodeInfo("TGETS", a="dst", b="var", c="str"),
  OpcodeInfo("TGETB", a="dst", b="var", c="lit"),
  OpcodeInfo("TGETR", a="dst", b="var", c="var"),
  OpcodeInfo("TSETV", a="var", b="var", c="var"),
  OpcodeInfo("TSETS", a="var", b="var", c="str"),
  OpcodeInfo("TSETB", a="var", b="var", c="lit"),
  OpcodeInfo("TSETM", a="base", d="num"),
  OpcodeInfo("TSETR", a="var", b="var", c="var"),

  # Calls and vararg handling. T = tail call.
  OpcodeInfo("CALLM", a="base", b="lit", c="lit"),
  OpcodeInfo("CALL", a="base", b="lit", c="lit"),
  OpcodeInfo("CALLMT", a="base", d="lit"),
  OpcodeInfo("CALLT", a="base", d="lit"),
  OpcodeInfo("ITERC", a="base", b="lit", c="lit"),
  OpcodeInfo("ITERN", a="base", b="lit", c="lit"),
  OpcodeInfo("VARG", a="base", b="lit", c="lit"),
  OpcodeInfo("ISNEXT", a="base", d="jump"),

  # Returns.
  OpcodeInfo("RETM", a="base", d="lit"),
  OpcodeInfo("RET", a="rbase", d="lit"),
  OpcodeInfo("RET0", a="rbase", d="lit"),
  OpcodeInfo("RET1", a="rbase", d="lit"),

  # Loops and branches. I/J = interp/JIT, I/C/L = init/call/loop.
  OpcodeInfo("FORI", a="base", d="jump"),
  OpcodeInfo("JFORI", a="base", d="jump"),
  OpcodeInfo("FORL", a="base", d="jump"),
  OpcodeInfo("IFORL", a="base", d="jump"),
  OpcodeInfo("JFORL", a="base", d="lit"),
  OpcodeInfo("ITERL", a="base", d="jump"),
  OpcodeInfo("IITERL", a="base", d="jump"),
  OpcodeInfo("JITERL", a="base", d="lit"),
  OpcodeInfo("LOOP", a="rbase", d="jump"),
  OpcodeInfo("ILOOP", a="rbase", d="jump"),
  OpcodeInfo("JLOOP", a="rbase", d="lit"),
  OpcodeInfo("JMP", a="rbase", d="jump"),

  # Function headers. I/J = interp/JIT, F/V/C = fixarg/vararg/C func.
  OpcodeInfo("FUNCF", a="rbase"),
  OpcodeInfo("IFUNCF", a="rbase"),
  OpcodeInfo("JFUNCF", a="rbase", d="lit"),
  OpcodeInfo("FUNCV", a="rbase"),
  OpcodeInfo("IFUNCV", a="rbase"),
  OpcodeInfo("JFUNCV", a="rbase", d="lit"),
  OpcodeInfo("FUNCC", a="rbase"),
  OpcodeInfo("FUNCCW", a="rbase"),
]

UNKNOWN_OPCODE_INFO = OpcodeInfo("UNKNWN")