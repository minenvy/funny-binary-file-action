from services.meter import get_meter_by_customer_and_cycle, get_meters_by_customer
from services.price import get_list_price
from utils.date import get_previous_cycle
from utils.system import print_error

def get_previous_cycle_meter(customer_id: str, cycle: str):
  previous_cycle_meter = None
  current_previous_cycle = cycle

  total_used_cycle_electric_of_customer = len(get_meters_by_customer(customer_id))

  if total_used_cycle_electric_of_customer == 1:
    return None

  while previous_cycle_meter == None:
    previous_cycle = get_previous_cycle(current_previous_cycle)
    previous_cycle_meter = get_meter_by_customer_and_cycle(customer_id, previous_cycle)
    current_previous_cycle = previous_cycle
  
  return previous_cycle_meter

def calculate_used_meter_of_cycle(customer_id: str, cycle: str) -> float:
  current_cycle_meter = get_meter_by_customer_and_cycle(customer_id, cycle)
  if current_cycle_meter == None:
    print_error(f'Chi so dien cua khach hang ky {cycle} chua chot')
    return 0
  
  total_used_cycle_electric_of_customer = len(get_meters_by_customer(customer_id))
  if total_used_cycle_electric_of_customer == 1:
    return current_cycle_meter['electricity_index']

  previous_cycle_meter = get_previous_cycle_meter(customer_id, cycle)

  if previous_cycle_meter == None:
    return current_cycle_meter['electricity_index']
  
  return current_cycle_meter['electricity_index'] - previous_cycle_meter['electricity_index']

def calculate_price_of_electricity(customer_id: str, cycle: str):
  prices = get_list_price()
  sorted_prices = dict(sorted(prices.items()))

  used_meter = calculate_used_meter_of_cycle(customer_id, cycle)
  total = 0

  for _, price in sorted_prices.items():
    if used_meter >= price['from_index'] and used_meter <= price['to_index']:
      total += price['price'] * (used_meter - price['from_index'])
    elif used_meter >= price['from_index'] and price['to_index'] == 0:
      total += price['price'] * (used_meter - price['from_index'])
    elif used_meter >= price['from_index'] and used_meter > price['to_index']:
      total += price['price'] * (price['to_index'] - price['from_index'])
    else:
      continue

  return total

