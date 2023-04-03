def transform_str_to_int(str):
  num = 0
  if '만' in str:
    num = float(str[:-1]) * 10_000
  elif '억' in str:
    num = float(str[:-1]) * 100_000_000
  else:
    num = float(str)

  return num