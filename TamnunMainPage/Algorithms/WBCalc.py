"""This file serves as a hub for the Weight & Balance algorithms. import this file to a view for
    access to these algorithms"""
import json
import numpy as np
from .DerivativeGrenerator import Derivative_Grenerator
import operator
# from .LimitsFinder import fuel_in_envelope_bisection


def apply_safety_factors(W_SF, CG_SF, weight, CG, Tail_num, MAC=None):
    """Applies safety factors to TN data

    Arguments:
        W_SF {float}
        CG_SF {float}
        weight {float}
        CG {float} -- can be either Long. or Lat.
        Tail_num {string} -- TN itself (e.g: 202,907 ... )

    Keyword Arguments:
        MAC {float} -- MAC value, for fixed wing A/C (default: {None})

    Returns:
        [dict] -- dictionary containing the SF values with matching signs 
    """
    tn = {
        "Tail_num": [
            Tail_num + " ++",
            Tail_num + " -+",
            Tail_num + " --",
            Tail_num + " +-",
        ]
    }

    if MAC is not None:
        CG_SF_MAC = (CG_SF / 100) * MAC

        p1 = [weight * (1 + (W_SF / 100)), CG + CG_SF_MAC]  # heavy, aft
        p2 = [weight * (1 - (W_SF / 100)), CG + CG_SF_MAC]  # light, aft
        p3 = [weight * (1 - (W_SF / 100)), CG - CG_SF_MAC]  # light, forward
        p4 = [weight * (1 + (W_SF / 100)), CG - CG_SF_MAC]  # heavy, forward

        return [
            tn,
            {"Weight": [p1[0], p2[0], p3[0], p4[0]]},
            {"CG": [p1[1], p2[1], p3[1], p4[1]]},
        ]

    p1 = [weight * (1 + (W_SF / 100)), CG + CG_SF]
    p2 = [weight * (1 - (W_SF / 100)), CG + CG_SF]
    p3 = [weight * (1 - (W_SF / 100)), CG - CG_SF]
    p4 = [weight * (1 + (W_SF / 100)), CG - CG_SF]

    return [
        tn,
        {"Weight": [p1[0], p2[0], p3[0], p4[0]]},
        {"CG": [p1[1], p2[1], p3[1], p4[1]]},
    ]


def list_discrete_configs(client_request):
    """Converts client choices to discrete configurations

    Arguments:
        client_request {dict} -- deserialized JSON object holding the user's choices

    Returns:
        discrete_configs [list] -- list of dicts
    """
    try:
        server_data = json.loads(client_request)
        discrete_configs = Derivative_Grenerator(server_data)
    except json.JSONDecodeError as error:
        print("Error deserialize client request", error)
        return {}
    except TypeError as error:
        print("Error deserialize client request", error)
        return {}
    else:
        return discrete_configs


def add_config_to_fuelflow(fuelflow, config_data):
    try:
        fuelflow_weight = fuelflow["weight"]
        fuelflow_moment_long = fuelflow["moment_long"]
        config_moment_long = config_data["Weight"] * config_data["CG"]
    except KeyError:
        print("KeyError: check if 'weight','moment_long','CG' keys exist ")
        return config_data
    config_moment_long = config_data["Weight"] * config_data["CG"]
    centrogram = {
        "name": config_data["items"], "weight": [], "cg_long": []}
    config_moment_long = config_data["Weight"] * config_data["CG"]

    for weight, moment in list(zip(fuelflow_weight, fuelflow_moment_long)):
        centrogram["weight"].append(weight + config_data["Weight"])
        centrogram["cg_long"].append(
            ((moment + config_moment_long) /
                (weight + config_data["Weight"]))
        )
    return centrogram


def create_centrograms_from_configs(config, fuelflow):
    centrograms = []
    for tn_item in config:
        for derivative in tn_item["Derivatives"]:
            centrograms.append(add_config_to_fuelflow(fuelflow, derivative))
    return centrograms


def filter_centrograms(centrograms, envelope):
    pass


def get_limits_from_centrogram(centrogram, envelope):
    pass


def get_most_strict_limits(limits):
    takeoff_limits = [limit["takeoff_fuel"] for limit in limits]
    landing_limits = [limit["landing_fuel"] for limit in limits]

    return [min(takeoff_limits), max(landing_limits)]


def perform_WB_calc(parsed_client_request):
    """
    flow:
    1. get parsed data from user
    2. apply SF
    3. ready up data for calculation
    4. calculate and filter
    5. get most strict limits
    6. send to user

    """
    pass


if __name__ == "__main__":
    """Testing script - delete in prod
    """
    import json

    with open(
        "C:\\Tamnun\\TAMNUN_DEV\\TamnunProject\\TamnunMainPage\\DummyData\\DerivativeGeneratorTest1.json"
    ) as f:
        configs = json.loads(f.read())
    with open(
        "C:\\Tamnun\\TAMNUN_DEV\\TamnunProject\\TamnunMainPage\\DummyData\\fuelflow1.json"
    ) as f:
        fuelflow = json.loads(f.read())

    # centrograms = CentrogramUtilites.create_cenrogram_from_configs(configs, fuelflow)
    centrograms = create_cenrogram_from_configs(configs, fuelflow)
    with open(
        "C:\\Tamnun\\TAMNUN_DEV\\TamnunProject\\TamnunMainPage\\DummyData\\centrograms1.json",
        "w",
    ) as f:
        f.write(json.dumps(centrograms))
