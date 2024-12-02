import os
import csv


def write_csv(path: str, data: dict, fields: list) -> None:
    if not os.path.exists(path):
        with open(path, mode='w+', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerow(data)
    else:
        with open(path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writerow(data)
