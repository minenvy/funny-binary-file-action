from constants.index import TAX
from services.bill import Bill, find_bill_by_customer_id, update_bill_or_create_if_not_exist
from services.customer import Customer, CustomerUpdate, create_customer, delete_customer, get_customer_by_id, update_customer
from services.meter import Meter, MeterUpdate, create_meter, delete_meter, get_meter_by_customer_and_cycle, update_meter, validate_cycle_for_meter
from services.price import Price, PriceUpdate, create_price, delete_price, get_price_by_level, update_price
from utils.date import validate_cycle, validate_date_string
from utils.price import calculate_price_of_electricity, calculate_used_meter_of_cycle, get_previous_cycle_meter, read_vietnamese_number
from utils.questionary import get_selection_answer, get_text_answer_with_validation
from utils.system import print_error, print_title

def show_main_menu_action():
  return get_selection_answer(
    "Menu chinh: ", 
    [
      {
        "option": "Thao tac du lieu", 
        "next_step": "15"
      }, 
      {
        "option": "Tinh dien nang tieu thu cua mot khach hang", 
        "next_step": "14"
      },
      {
        "option": "Tim kiem du lieu", 
        "next_step": "16"
      },
      {
        "option": "Tinh tien dien trong ky cua mot khach hang", 
        "next_step": "20"
      },
      {
        "option": "In hoa don tien dien trong ky cua mot khach hang", 
        "next_step": "21"
      },
    ],
    can_exit = True
  )

def show_customer_menu_action():
  return get_selection_answer(
    "Menu khach hang: ", 
    [
      {
        "option": "Them khach hang", 
        "next_step": "5"
      },
      {
        "option": "Cap nhat khach hang", 
        "next_step": "6"
      },
      {
        "option": "Xoa khach hang", 
        "next_step": "7"
      },
    ]
  )

def show_meter_menu_action():
  return get_selection_answer(
    "Menu chi so dien: ", 
    [
      {
        "option": "Them chi so dien", 
        "next_step": "8"
      },
      {
        "option": "Cap nhat chi so dien", 
        "next_step": "9"
      },
      {
        "option": "Xoa chi so dien", 
        "next_step": "10"
      },
    ]
  )

def show_price_menu_action():
  return get_selection_answer(
    "Menu gia dien: ", 
    [
      {
        "option": "Them gia dien", 
        "next_step": "11"
      },
      {
        "option": "Cap nhat gia dien", 
        "next_step": "12"
      },
      {
        "option": "Xoa gia dien", 
        "next_step": "13"
      },
    ]
  )

def create_customer_action():
  print_title("Them khach hang")
  customer_id = get_text_answer_with_validation("Nhap ma khach hang: ", lambda customer_id: not get_customer_by_id(customer_id), "Ma khach hang da ton tai, moi nhap lai")  
  customer_name = input("Nhap ten khach hang: ")
  customer_address = input("Nhap dia chi khach hang: ")
  customer_meter_id = input("Nhap ma cong to dien khach hang: ")

  customer = create_customer(Customer(id=customer_id, name=customer_name, address=customer_address, meter_id=customer_meter_id))
  if customer:
    print("Them khach hang thanh cong")

def update_customer_action():
  print_title("Cap nhat khach hang")
  customer_id = get_text_answer_with_validation("Nhap ma khach hang: ", get_customer_by_id, "Khong tim thay khach hang, moi nhap lai")  
  customer_name = input("Nhap ten khach hang (Enter de bo qua): ")
  customer_address = input("Nhap dia chi khach hang (Enter de bo qua): ")
  customer_meter_id = input("Nhap ma cong to dien khach hang (Enter de bo qua): ")

  updated_customer = {}
  if (customer_name != ""):
    updated_customer['name'] = customer_name
  if (customer_address != ""):
    updated_customer['address'] = customer_address
  if (customer_meter_id != ""):
    updated_customer['meter_id'] = customer_meter_id

  update_customer(customer_id, CustomerUpdate(**updated_customer))
  print('Cap nhat khach hang thanh cong')

def delete_customer_action():
  print_title("Xoa khach hang")
  customer_id = input("Nhap ma khach hang: ")
  delete_customer(customer_id)
  print('Xoa khach hang thanh cong')

def create_meter_action():
  print_title("Them chi so dien")
  customer_id = input("Nhap ma khach hang: ")
  electricity_index = float(get_text_answer_with_validation("Nhap chi so dien: ", float, "Chi so dien khong hop le, moi nhap lai"))
  closing_date = get_text_answer_with_validation("Nhap ngay chot (dd/mm/yyyy): ", validate_date_string)
  cycle = get_text_answer_with_validation("Nhap ky (mm/yyyy): ", lambda cycle: validate_cycle_for_meter(cycle, customer_id), "Ky khong hop le hoac da bi trung lap, moi nhap lai")

  meter = create_meter(Meter(customer_id=customer_id, electricity_index=electricity_index, closing_date=closing_date, cycle=cycle))
  if meter:
    print("Them chi so dien thanh cong")

def update_meter_action():
  print_title("Cap nhat chi so dien")
  customer_id = input("Nhap ma khach hang: ")
  cycle = get_text_answer_with_validation("Nhap ky (mm/yyyy): ", lambda cycle: get_meter_by_customer_and_cycle(customer_id, cycle), "Khong tim thay thong tin dien ky nay, moi nhap lai")
  electricity_index = input("Nhap chi so dien (Enter de bo qua): ")
  closing_date =input("Nhap ngay chot (dd/mm/yyyy) (Enter de bo qua): ")

  updated_meter = {}
  if (electricity_index != ""):
    updated_meter['electricity_index'] = electricity_index
  if (closing_date != ""):
    updated_meter['closing_date'] = closing_date

  update_meter(customer_id, cycle, MeterUpdate(**updated_meter))
  print('Cap nhat chi so dien thanh cong')

def delete_meter_action():
  print_title("Xoa chi so dien")
  customer_id = input("Nhap ma khach hang: ")
  cycle = get_text_answer_with_validation("Nhap ky (mm/yyyy): ", lambda cycle: validate_cycle_for_meter(cycle, customer_id), "Ky khong hop le, moi nhap lai")

  delete_meter(customer_id, cycle)
  print('Xoa chi so dien thanh cong')

def create_price_action():
  print_title("Them gia dien")
  level = get_text_answer_with_validation("Nhap bac gia dien: ", lambda level: int(level) and get_price_by_level(level) == None, "Bac gia dien phai la mot so nguyen va khong trung lap, moi nhap lai")
  from_index = float(get_text_answer_with_validation("Nhap chi so dau: ", float, "Chi so dau khong hop le, moi nhap lai"))
  to_index = float(get_text_answer_with_validation("Nhap chi so cuoi: ", float, "Chi so cuoi khong hop le, moi nhap lai"))
  price = float(get_text_answer_with_validation("Nhap gia tien/so dien: ", float, "Gia tien khong hop le, moi nhap lai"))

  price = create_price(Price(level=level, from_index=from_index, to_index=to_index, price=price))
  if price:
    print("Them gia dien thanh cong")

def update_price_action():
  print_title("Cap nhat gia dien")
  level = get_text_answer_with_validation("Nhap bac gia dien: ", get_price_by_level)
  from_index = input("Nhap chi so dau (Enter de bo qua): ")
  to_index = input("Nhap chi so cuoi (Enter de bo qua): ")
  price = input("Nhap gia tien/so dien (Enter de bo qua): ")

  updated_price = {}
  if (from_index != ""):
    updated_price['from_index'] = from_index
  if (to_index != ""):
    updated_price['to_index'] = to_index
  if (price != ""):
    updated_price['price'] = price

  update_price(level, PriceUpdate(**updated_price))
  print('Cap nhat gia dien thanh cong')

def delete_price_action():
  print_title("Xoa gia dien")
  level = get_text_answer_with_validation("Nhap bac gia dien: ", get_price_by_level)

  delete_price(level)
  print('Xoa gia dien thanh cong')

def calculate_used_meter_of_specific_month_action():
  print_title("Tinh so dien nang da su dung")
  customer_id = get_text_answer_with_validation("Nhap ma khach hang: ", get_customer_by_id, "Khong tim thay khach hang, moi nhap lai")  
  cycle = get_text_answer_with_validation("Nhap ky (mm/yyyy): ", validate_cycle, "Ky khong hop le, moi nhap lai")

  print(f"Chi so dien da su dung ky {cycle}: {calculate_used_meter_of_cycle(customer_id, cycle)}")

def show_search_menu_action():
  return get_selection_answer(
    "Tim kiem thong tin: ", 
    [
      {
        "option": "Tra cuu thong tin khach hang", 
        "next_step": "17"
      }, 
      {
        "option": "Tra cuu thong tin dien nang tieu thu cua khach hang trong mot ky", 
        "next_step": "18"
      },
    ]
  )

def show_operation_data_menu_action():
  return get_selection_answer(
    "Thao tac du lieu: ", 
    [
      {
        "option": "Thao tac khach hang", 
        "next_step": "2"
      }, 
      {
        "option": "Thao tac chi so dien", 
        "next_step": "3"
      },
      {
        "option": "Thao tac gia dien", 
        "next_step": "4"
      },
    ]
  )

def search_customer_action():
  print_title("Tra cuu thong tin khach hang")
  customer_id = input("Nhap ma khach hang: ")
  customer = get_customer_by_id(customer_id)

  if not customer:
    print_error("Khong tim thay khach hang")
  else:
    print(f'Ten khach hang: {customer['name']}')
    print(f'Dia chi khach hang: {customer['address']}')
    print(f'Ma cong to dien khach hang: {customer['meter_id']}')

def search_meter_action():
  print_title("Tra cuu thong tin dien nang tieu thu cua khach hang trong mot ky")
  customer_id = get_text_answer_with_validation("Nhap ma khach hang: ", get_customer_by_id, "Khong tim thay khach hang, moi nhap lai")  
  cycle = get_text_answer_with_validation("Nhap ky (mm/yyyy): ", validate_cycle, "Ky khong hop le, moi nhap lai")
  meter = get_meter_by_customer_and_cycle(customer_id, cycle)

  if not meter:
    print_error("Khong tim thay thong tin dien nang")
  else:
    print(f"Chi so dien cuoi ky {cycle}: {meter['electricity_index']}")
    print(f"Ngay chot: {meter['closing_date']}")
    print(f"Ky: {meter['cycle']}")

def calculate_electricity_price_of_specific_month_action():
  print_title("Tinh tien dien")
  customer_id = get_text_answer_with_validation("Nhap ma khach hang: ", get_customer_by_id, "Khong tim thay khach hang, moi nhap lai")  
  cycle = get_text_answer_with_validation("Nhap ky (mm/yyyy): ", lambda cycle: validate_cycle_for_meter(cycle, customer_id), "Ky khong hop le, moi nhap lai")

  latest_meter = get_meter_by_customer_and_cycle(customer_id, cycle)
  if not latest_meter:
    print_error(f"Khong tim thay thong tin dien nang ky {cycle}")
    return

  previous_cycle = get_previous_cycle_meter(customer_id, cycle)
  previous_meter = None
  if previous_cycle:
    previous_meter = get_meter_by_customer_and_cycle(customer_id, previous_cycle['cycle'])
  
  used_meter = latest_meter['electricity_index'] - previous_meter['electricity_index'] if previous_meter else latest_meter['electricity_index']
  total = calculate_price_of_electricity(customer_id, cycle)

  update_bill_or_create_if_not_exist(Bill(customer_id=customer_id, cycle=cycle, from_date=previous_meter['closing_date'] if previous_meter else 'N/A', to_date=latest_meter['closing_date'] if latest_meter else 'N/A', power_consumption=used_meter, total=total))
  print('Tien dien da duoc ghi vao file HOADON')

def show_menu_calculate_electricity():
  return get_selection_answer(
    "Menu hoa don tien dien mot ky: ", 
    [
      {
        "option": "Tinh tien dien", 
        "next_step": "20"
      }, 
      {
        "option": "In hoa don tien dien", 
        "next_step": "23"
      },
    ]
  )

def show_calculate_electricity_bill_recently():
  print_title("In hoa don tien dien")
  customer_id = get_text_answer_with_validation("Nhap ma khach hang: ", get_customer_by_id, "Khong tim thay khach hang, moi nhap lai")

  bill = find_bill_by_customer_id(customer_id)
  if not bill:
    print_error("Khong tim thay thong tin hoa don cua khach hang nay")
    return

  customer = get_customer_by_id(customer_id)
  used_meter = bill['power_consumption']
  total = bill['total'] * (1 + TAX)

  if customer:
    print(f"Ma khach hang: {customer_id}")
    print(f"Ten khach hang: {customer['name']}")
    print(f"Dia chi khach hang: {customer['address']}")
    print(f"Ma so cong to: {customer['meter_id']}")
    print(f"Ky: {bill['cycle']}")
    print(f"Tu ngay {bill['from_date'] or 'N/A'} den {bill['to_date'] or 'N/A'}")
    print(f"Chi so dien da su dung ky {bill['cycle']}: {used_meter}")
    print(f"Tong tien dien ky {bill['cycle']} (chua bao gom thue): {int(bill['total'])}")
    print(f"Thue: {100 * TAX}%")
    print(f"Tong tien dien ky {bill['cycle']} (bao gom thue): {int(total)}")
    print(f"Tong tien bang chu: {read_vietnamese_number(int(total))}")
    