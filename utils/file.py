import json
from pathlib import Path
from typing import List

current_file = Path(__file__).resolve()
utils_dir = current_file.parent.parent
data_folder_path = utils_dir / 'data'

def get_file_path(file_name: str) -> Path:
  return data_folder_path / file_name

def rewrite_binary_file(file_path: str, data: dict) -> None:
  """
  Writes a given data structure to a binary file

  Args:
    file_path (str): The path to the file to write to
    data (dict): The data structure to write
  """
  file_path_inside_data_folder = get_file_path(file_path)
  # Convert the given data to a string
  json_string = json.dumps(data)
  
  # Convert each character of the string to 8-bit binary
  binary_str = ''.join(format(ord(char), '08b') for char in json_string)

  # Write the binary string to the file
  with open(file_path_inside_data_folder, 'wb') as file:
    file.write(binary_str.encode())

def read_binary_file(file_path: str) -> dict:
  """
  Reads a binary file and converts its data to a string and then a JSON object

  Args:
    file_path (str): The path to the file to read from

  Returns:
    dict: A JSON object containing the data from the file
  """
  file_path_inside_data_folder = get_file_path(file_path)
  with open(file_path_inside_data_folder, 'rb') as file:
    # Read the binary data
    data = file.read()

    # Split the data into 8-bit chunks
    bytes_list = [data[i:i+8] for i in range(0, len(data), 8)]

    # Convert the chunks back to bytes
    byte_values = bytes(int(b, 2) for b in bytes_list)

    # Decode the bytes using UTF-8
    utf8_string = byte_values.decode('utf-8')

    # Parse the string as JSON
    json_data = json.loads(utf8_string or "{}")

    return json_data

def write_to_empty_text_file(file_path: str, text: str) -> None:
  file_path_inside_data_folder = get_file_path(file_path)
  with open(file_path_inside_data_folder, "a") as f:
    f.write(f"{text}\n")

def read_json_file(file_path: str) -> dict:
  file_path_inside_data_folder = get_file_path(file_path)
  with open(file_path_inside_data_folder, "r") as file:
    return json.load(file)

def rewrite_list_text_to_binary_file(file_path: str, data: List[str]) -> None:
  text = ''.join(data)
  # Convert each character of the string to 8-bit binary
  binary_str = ''.join(format(ord(char), '08b') for char in text)

  file_path_inside_data_folder = get_file_path(file_path)
  # Write the binary string to the file
  with open(file_path_inside_data_folder, 'wb') as file:
    file.write(binary_str.encode())

def read_list_text_from_binary_file(file_path: str):
  """
  Reads a binary file and converts its data to a string and then a JSON object

  Args:
    file_path (str): The path to the file to read from

  Returns:
    dict: A JSON object containing the data from the file
  """
  file_path_inside_data_folder = get_file_path(file_path)
  with open(file_path_inside_data_folder, 'rb') as file:
    # Read the binary data
    data = file.read()

    # Split the data into 8-bit chunks
    bytes_list = [data[i:i+8] for i in range(0, len(data), 8)]

    # Convert the chunks back to bytes
    byte_values = bytes(int(b, 2) for b in bytes_list)

    # Decode the bytes using UTF-8
    utf8_string = byte_values.decode('utf-8')

    return utf8_string
