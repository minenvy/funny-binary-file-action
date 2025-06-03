import utils.action as actions
from utils.file import read_json_file

def load_menu_data():
  return read_json_file("menu.json")

def get_action_by_name(name: str):
  func = getattr(actions, name, None)

  if callable(func):
    return func
  else:
    return lambda: None
