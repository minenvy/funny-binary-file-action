import builtins
import re
from utils.file import write_to_empty_text_file

def print_title(title: str):
  print("\033[32m" + title + "\033[0m")

def print_error(error: str):
  print("\033[31m" + error + "\033[0m")

def remove_ansi_codes(text):
  ansi_escape = re.compile(r'\033\[\d+m')
  return ansi_escape.sub('', text)

def make_custom_in_out():
  # Backup original functions
  original_print = builtins.print
  original_input = builtins.input

  def custom_print(*args, **kwargs):
    # Build the message
    message = " ".join(str(arg) for arg in args)

    # Write to log file
    write_to_empty_text_file('log.txt', f"He thong: {remove_ansi_codes(message)}")

    # Call the original print (to still show in console)
    original_print(*args, **kwargs)

  def custom_input(prompt=""):
    # Show prompt using original print to avoid recursion
    original_print(prompt, end="")  # mimic input(prompt)

    user_input = original_input()

    # Log the prompt and response
    write_to_empty_text_file('log.txt', f"He thong: {prompt}")
    write_to_empty_text_file('log.txt', f"Nguoi dung: {user_input}")

    return user_input

  # Override built-in functions
  builtins.print = custom_print
  builtins.input = custom_input
