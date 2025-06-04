from typing import List, Dict

from utils.system import print_error

invalid_message = "Du lieu khong hop le. Vui long chon lai."

def get_text_answer(question: str) -> str:
  return input(question)

def get_text_answer_with_validation(question: str, validateFunction, invalid_message: str = invalid_message) -> str:
  text = ''
  while text == '':
    text = input(question)
    if (not validateFunction(text)):
      print_error(invalid_message)
      text = ''
  return text

def get_number_answer(question: str) -> float:
  number = input(question)
  if number.isdigit():
    return float(number)
  else:
    print_error(invalid_message)
    return get_number_answer(question)

def get_selection_answer(question: str, choices: List[Dict[str, str]], can_exit: bool = False) -> str:
  print("\033[32m" + question + "\033[0m")
  for i, choice in enumerate(choices):
    print(f"{i + 1}. {choice['option']}")
  print(f"0. {'Thoat' if can_exit else 'Tro lai'}")

  number_of_questions = len(choices)
  choice_index = input(f"Chon mot gia tri (0-{number_of_questions}): ")

  if '0' < choice_index <= str(number_of_questions):
    return choices[int(choice_index) - 1]['next_step']
  elif choice_index == '0':
    return '0'
  else:
    print_error(invalid_message)
    return get_selection_answer(question, choices)  

