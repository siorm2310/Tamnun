import sys
import json
from .WBCalc import perform_WB_calc as WBCalc


# python CLI.py -file / -arg [data]

def calc_from_file(json_file):
    with open(json_file, 'r') as f:
        parsed_json = json.loads(f)
    results = WBCalc(parsed_json)
    print(results)
    print("calc_from_file")


def calc_from_args(json_args):
    parsed_json = json.loads(json_args)
    results = WBCalc(parsed_json)
    print(results)
    print("calc_from_args")


args = sys.argv[1:]
print(args)

try:
    options = {
        "-file": calc_from_file,
        "-arg": calc_from_args
    }[args[0]](args[1])
except KeyError as error:
    print(f"Wrong keys. You provided the key {error}. Please enter '-file' or '-arg' as flags")
