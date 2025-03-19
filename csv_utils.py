import os
import csv
import re

def sanitize_filename(filename: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def write_csv(path: str, data: dict, fields: list) -> None:
    directory_path = os.path.dirname(path)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)
        
    if not os.path.exists(path):
        with open(path, mode='w+', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerow(data)
    else:
        with open(path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writerow(data)