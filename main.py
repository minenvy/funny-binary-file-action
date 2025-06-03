from constants.index import INITIAL_STEP, EXIT_STEP
from utils.menu import get_action_by_name, load_menu_data
from utils.system import make_custom_in_out

make_custom_in_out()

current_step = INITIAL_STEP
menu = load_menu_data()

while current_step != '0':
  action = get_action_by_name(menu[str(current_step)]['action_name'])
  next_step = action()

  if current_step == INITIAL_STEP and next_step == EXIT_STEP:
    print('Thoat chuong trinh!')
    break

  if next_step == EXIT_STEP or next_step == None:
    current_step = menu[str(current_step)]['parent_step']
    continue

  current_step = next_step
