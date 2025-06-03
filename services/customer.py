from typing import Optional
from dataclasses import dataclass, asdict
from constants.index import FILE_DATA_NAMES
from utils.file import read_binary_file, rewrite_binary_file

customer_file_name: str = FILE_DATA_NAMES['kh']

@dataclass
class Customer:
  id: str
  name: str
  address: str
  meter_id: str

@dataclass
class CustomerUpdate:
  name: Optional[str] = None
  address: Optional[str] = None
  meter_id: Optional[str] = None

def create_customer(customer: Customer):
  customers = read_binary_file(customer_file_name)

  if (customer.id in customers):
    print("Customer already exists")
    return
  
  new_customer = asdict(customer)
  customers[customer.id] = new_customer
  rewrite_binary_file(customer_file_name, customers)

  return customer

def get_customer_by_id(customer_id: str):
  customers = read_binary_file(customer_file_name)
  return customers.get(customer_id)

def update_customer(customer_id: str, customer: CustomerUpdate):
  customers = read_binary_file(customer_file_name)

  # Convert stored dict to Customer instance
  existing_customer = Customer(**customers[customer_id])

  # Convert update dataclass to dict, filter out None fields
  update_data = {k: v for k, v in asdict(customer).items() if v is not None}

  # Merge existing customer dict with update data
  updated_dict = {**asdict(existing_customer), **update_data}

  # Save updated customer dict back to customers
  customers[customer_id] = updated_dict

  rewrite_binary_file(customer_file_name, customers)

  return updated_dict
  

def delete_customer(customer_id: str):
  customers = read_binary_file(customer_file_name)
  customer = customers.get(customer_id)

  if customer:
    del customers[customer_id]
    rewrite_binary_file(customer_file_name, customers)

  return customer