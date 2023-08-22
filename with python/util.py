import sys, time

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

def print_progress(iteration, total, start_time, try_cnt, prefix='', suffix='', decimals=1, bar_length=100):
  format_str = "{0:." + str(decimals) + "f}"
  percent = format_str.format(100 * (iteration / float(total)))
  filled_length = int(round(bar_length * iteration / float(total)))
  bar = '#' * filled_length + '-' * (bar_length - filled_length)

  elapsed_time = time.time() - start_time
  hours = int(elapsed_time // 3600)
  minutes = int((elapsed_time % 3600) // 60)
  seconds = int(elapsed_time % 60)
  milliseconds = int((elapsed_time % 1) * 1000)

  elapsed_time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}"

  sys.stdout.write('\r%s |%s| %s%s %s [%s/%s] [try: %s], Elapesed Time: %s' % (prefix, bar, percent, '%', suffix, format(iteration, ','), format(total, ','), format(try_cnt, ','), elapsed_time_str))
  if iteration == total:
    sys.stdout.write('\n')
  sys.stdout.flush()
