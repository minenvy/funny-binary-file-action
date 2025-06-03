from typing import Optional
from dataclasses import dataclass, asdict
from constants.index import FILE_DATA_NAMES
from utils.file import read_binary_file, rewrite_binary_file

price_file_name: str = FILE_DATA_NAMES['gia_dien']

@dataclass
class Price:
  level: str
  from_index: float
  to_index: float
  price: float

@dataclass
class PriceUpdate:
  from_index: Optional[float] = None
  to_index: Optional[float] = None
  price: Optional[float] = None

def create_price(price: Price):
  prices = read_binary_file(price_file_name)

  if (price.level in prices):
    print("Price already exists")
    return
  
  new_price = asdict(price)
  prices[price.level] = new_price
  rewrite_binary_file(price_file_name, prices)

  return price

def get_list_price():
  prices = read_binary_file(price_file_name)
  return prices

def get_price_by_level(price_level: str):
  prices = read_binary_file(price_file_name)
  return prices.get(price_level)

def update_price(price_level: str, price: PriceUpdate):
  prices = read_binary_file(price_file_name)

  existing_price = Price(**prices[price_level])
  update_data = {k: v for k, v in asdict(price).items() if v is not None}
  new_price = {**asdict(existing_price), **update_data}
  prices[price_level] = new_price

  rewrite_binary_file(price_file_name, prices)

  return new_price
  

def delete_price(price_level: str):
  prices = read_binary_file(price_file_name)
  price = prices.get(price_level)

  if price:
    del prices[price_level]
    rewrite_binary_file(price_file_name, prices)

  return price