def is_real_value(value):
  if value is None:
    return False
  elif isinstance(value, str):
    return value.strip() != ""
  elif isinstance(value, int):
    return True