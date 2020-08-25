"""
This tool is used for bulk updating the DB using a CSV file or a .json file.
Select your model, your data type and upload it to the DB   
"""
import csv
import json
import sys
# from TamnunMainPage.models import Item, ItemGroup, Aircraft, FuelFlow, Envelope
# TODO: Object validation, register the file for DB changes
try:
    options = {
        "ItemGroup": ItemGroup,
        "Aircraft": Aircraft,
        "Item": Item,
        "FuelFlow": FuelFlow,
        "Envelope": Envelope,

    }
except KeyError as err:
    print("Please enter a valid object")


def update_with_json():
    print("You chose json")
    # json_path = input("Enter for path of json object: ")


def update_with_csv():
    pass


if __name__ == "__main__":
    print("Welcome to the DB update command line interface.\nUse this tool for bulk creation of model instances.")
    print("Types of objects allowed : Item,ItemGroup,Aircraft,FuelFlow,Envelope\n")
    input_model = input("Enter model to be updated : ")
    input_type = input("Enter updating option [json / csv] : ")

    try:
        options = {
            "json": update_with_json,
            "csv": update_with_csv
        }[input_type]
    except KeyError as err:
        print("Please enter a valid value [json / csv]")

    options()
