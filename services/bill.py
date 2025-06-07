from typing import Optional
from dataclasses import dataclass, asdict
from constants.index import FILE_DATA_NAMES
from utils.file import read_binary_file, rewrite_binary_file

bill_file_name: str = FILE_DATA_NAMES['hoa_don']

@dataclass
class Bill:
  customer_id: str
  cycle: str
  from_date: str
  to_date: str
  power_consumption: float
  total: float

def update_bill_or_create_if_not_exist(bill: Bill):
  bills = read_binary_file(bill_file_name)

  if (bill.customer_id in bills):
    updated_bill = update_bill(bill)
    return updated_bill
  
  created_bill = create_bill(bill)
  return created_bill

def create_bill(bill: Bill):
  bills = read_binary_file(bill_file_name)
  
  new_bill = asdict(bill)
  bills[bill.customer_id] = new_bill
  rewrite_binary_file(bill_file_name, bills)

  return bill

def update_bill(bill: Bill):
  bills = read_binary_file(bill_file_name)

  existing_bill = Bill(**bills[bill.customer_id])
  update_data = {k: v for k, v in asdict(bill).items() if v is not None}
  updated_dict = {**asdict(existing_bill), **update_data}
  bills[bill.customer_id] = updated_dict

  rewrite_binary_file(bill_file_name, bills)

  return updated_dict

def find_bill_by_customer_id(customer_id: str):
  bills = read_binary_file(bill_file_name)
  return bills.get(customer_id)
  