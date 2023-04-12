import sys

def transform_str_to_int(str):
  num = 0
  if '만' in str:
    num = float(str[:-1]) * 10_000
  elif '억' in str:
    num = float(str[:-1]) * 100_000_000
  elif 'K' in str:
    num = float(str[:-1]) * 1_000
  elif 'M' in str:
    num = float(str[:-1]) * 1_000_000
  else:
    num = float(str.replace(',', ''))

  return num

def print_progress(iteration, total, try_cnt, prefix = '', suffix = '', decimals = 1, bar_length  = 100):
  format_str = "{0:." + str(decimals) + "f}"
  percent = format_str.format(100 * (iteration / float(total)))
  filled_length = int(round(bar_length * iteration / float(total)))
  bar = '#' * filled_length + '-' * (bar_length - filled_length)

  sys.stdout.write('\r%s |%s| %s%s %s [%s/%s] [try: %s]' % (prefix, bar, percent, '%', suffix, iteration, total, try_cnt)),
  if iteration == total:
    sys.stdout.write('\n')
  sys.stdout.flush()