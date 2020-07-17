"""
This tool is used for bulk updating the DB using a CSV file or a .json file.
Select your model, your data type and upload it to the DB   
"""
import json
import csv
from .models import *

print("Welcome to the DB update command line interface.\nUse this tool for bulk update or creation of model instances.\n")
input_model = input("Enter model to be updated : ")
operation_type = input("Enter mode [update / create] : ")
input_type = input("Enter updating option [json / csv] : ")

try:
    options = {
        "json": update_with_json,
        "csv": update_with_csv
    }[input_type]
except KeyError as err:
    print("Please enter a valid value [json / csv]")
# TODO: Object validation, register the file for DB changes


def update_with_json():
    json_path = input("Enter for path of json object: ")


def update_with_csv():
    pass
