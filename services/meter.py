from dataclasses import dataclass, asdict
from typing import Optional
from constants.index import FILE_DATA_NAMES, DEFAULT_CYCLE
from utils.date import compare_greater_cycle, validate_cycle
from utils.file import read_binary_file, rewrite_binary_file

meter_file_name: str = FILE_DATA_NAMES['cs_dien']

@dataclass
class Meter:
  customer_id: str
  electricity_index: float
  closing_date: str
  cycle: str
  id: Optional[str] = None

@dataclass
class MeterUpdate:
  id: Optional[str] = None
  customer_id: Optional[str] = None
  electricity_index: Optional[float] = None
  closing_date: Optional[str] = None
  cycle: Optional[str] = None

def get_meter_id(customer_id: str, cycle: str):
  return customer_id + cycle

def create_meter(meter: Meter):
  meters = read_binary_file(meter_file_name)

  meter_id = get_meter_id(meter.customer_id, meter.cycle)
  if (meter_id in meters):
    print("Meter already exists")
    return
  
  new_meter = asdict(meter)
  new_meter['id'] = meter_id
  meters[meter_id] = new_meter
  rewrite_binary_file(meter_file_name, meters)

  return meter

def get_meter_by_customer_and_cycle(customer_id: str, cycle: str):
  meters = read_binary_file(meter_file_name)
  meter_id = get_meter_id(customer_id, cycle)
  return meters.get(meter_id)

def get_meters_by_customer(customer_id: str):
  meters = read_binary_file(meter_file_name)
  result = []
  for _, meter in meters.items():
    if meter['customer_id'] == customer_id:
      result.append(meter)
  return result

def update_meter(customer_id: str, cycle: str, meter: MeterUpdate):
  meters = read_binary_file(meter_file_name)

  meter_id = get_meter_id(customer_id, cycle)
  # Suppose Meter is your dataclass
  existing_meter = Meter(**meters[meter_id])

  # Convert update dataclass to dict and filter out None values
  update_data = {k: v for k, v in asdict(meter).items() if v is not None}

  # Merge existing meter dict with update_data
  new_meter = {**asdict(existing_meter), **update_data}

  # Save back
  meters[meter_id] = new_meter

  rewrite_binary_file(meter_file_name, meters)

  return new_meter
  

def delete_meter(customer_id: str, cycle: str):
  meters = read_binary_file(meter_file_name)
  meter_id = get_meter_id(customer_id, cycle)
  customer = meters.get(meter_id)

  if customer:
    del meters[meter_id]
    rewrite_binary_file(meter_file_name, meters)

  return customer

def validate_cycle_for_meter(cycle: str, customer_id: str):
  is_valid_cycle_format = validate_cycle(cycle)
  if not is_valid_cycle_format:
    exist_meter = get_meter_by_customer_and_cycle(customer_id, cycle)
    if exist_meter != None:
      return False
  return True

def get_latest_cycle_of_customer(customer_id: str):
  meters = read_binary_file(meter_file_name)
  latest_cycle = DEFAULT_CYCLE
  for _, meter in meters.items():
    if meter['customer_id'] == customer_id and compare_greater_cycle(meter['cycle'], latest_cycle):
      latest_cycle = meter['cycle']
  return latest_cycle