import re

def validate_date_string(date_str: str) -> bool:
  pattern = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/([0-9]{4})$'
  return bool(re.match(pattern, date_str))
  
def get_previous_cycle(cycle: str) -> str:
  month, year = cycle.split('/')
  month = int(month)
  year = int(year)
  if month == 1:
    year -= 1
    month = 12
  else:
    month -= 1
  return f"{month:02d}/{year:04d}"

def validate_cycle(date_str):
  pattern = r'^(0[1-9]|1[0-2])/([0-9]{4})$'
  return bool(re.match(pattern, date_str))

def compare_greater_cycle(first_cycle: str, second_cycle: str):
  first_month, first_year = first_cycle.split('/')
  second_month, second_year = second_cycle.split('/')

  return first_year > second_year or (first_year == second_year and int(first_month) > int(second_month))
