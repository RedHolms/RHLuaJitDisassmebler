import typing

class EnumMeta(type):
  def _find_value_path(self, target_value: typing.Any) -> str | None:
    path = None
    for value_name in self._get_all_enum_values_names():
      value = getattr(self, value_name)

      if type(value) == EnumMeta:
      # Sub-Enum
        sub_enum_path = value._find_value_path(target_value)
        if sub_enum_path == None:
          # this sub-enum does not contains this value
          continue
        else:
          # value is contained in this sub-enum
          path = f"{value_name}_" + sub_enum_path
          break
      elif value == target_value:
        # this enum contains target value
        return str(value_name)
    return path

  def _get_all_enum_values_names(self) -> list[str]:
    return [name for name in dir(self) if not name.startswith('_')]

  def __setattr__(self, name: str, value: typing.Any) -> None:
    # Enum is read-only
    return

  def __contains__(self, target_value: typing.Any) -> bool:
    for value_name in self._get_enum_values():
      value = getattr(self, value_name)
      if type(value) == EnumMeta and target_value in value:
        return True
      elif value == target_value:
        return True
    return False

  def __iter__(self):
    for attrName in self._get_enum_values():
      yield getattr(self, attrName)

class Enum(metaclass=EnumMeta):
  # we can't create instance of enum
	def __new__(cls, *args, **kwargs): return cls