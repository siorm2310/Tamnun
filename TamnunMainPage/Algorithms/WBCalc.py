"""This file serves as a hub for the Weight & Balance algorithms. import this file to a view for
    access to these algorithms"""
# from ..queries import WBQueries
# from .DerivativeGenerator import Derivative_Generator
from DerivativeGenerator import Derivative_Generator
import DerivativeGenerator
from LimitsFinder import fuel_limits_finder
import LimitsFinder
import json
import numpy as np
# from ..queries import WBQueries
# import ..queries


# from queries
# from django.shortcuts import get_object_or_404, get_list_or_404
# from modelsA import *
# import modelsA
# def get_WB_calc_data(tms):
#         aircraftType = get_object_or_404(AircraftType, TMS=tms)
#         try:
#             fuelFlows = FuelFlow.objects.filter(relatedAircraftType=aircraftType).values()
#             envelopes = Envelope.objects.filter(relatedAircraftType=aircraftType).values()
#         except:
#             print("Error retirieving fuelflows and envelopes")

#         data = {
#             "aircraftType": aircraftType,
#             "fuelFlows": list(fuelFlows),
#             "envelopes": list(envelopes),
#         }

#         return data

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
    print(tn)
    if MAC is not None:
        CG_SF_MAC = (CG_SF / 100) * MAC
        # ak=float(1+W_SF/100)
        


        # print(type(CG))
        p1 = [(float(weight) * float(1 + (W_SF / 100))), float(CG) + CG_SF_MAC]  # heavy, aft
        p2 = [float(weight) * float((1 - (W_SF / 100))), float(CG) + CG_SF_MAC]  # light, aft
        p3 = [float(weight) * float((1 - (W_SF / 100))), float(CG) - CG_SF_MAC]  # light, forward
        p4 = [float(weight) * float(1 + (W_SF / 100)), float(CG) - CG_SF_MAC]  # heavy, forward

        return [
            tn,
            {"Weight": [p1[0], p2[0], p3[0], p4[0]]},
            {"CG": [p1[1], p2[1], p3[1], p4[1]]},
        ]

    p1 = [float(weight) * float(1 + (W_SF / 100)), float(CG) + CG_SF]
    p2 = [float(weight) * float(1 - (W_SF / 100)), float(CG) + CG_SF]
    p3 = [float(weight) * float(1 - (W_SF / 100)), float(CG) - CG_SF]
    p4 = [float(weight) * float(1 + (W_SF / 100)), float(CG) - CG_SF]

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
        discrete_configs = Derivative_Generator(client_request)
    except json.JSONDecodeError as error:
        print("Error deserialize client request", error)
        return {}
    except TypeError as error:
        print("Error deserialize client request", error)
        return {}
    except KeyError as error:
        print("Error getting data's keys. check for correct input")
        print(error)
        return {}
    else:
        return discrete_configs


def add_config_to_fuelflow(fuelflow, config_data):
    try:
        fuelflow_weight = fuelflow[0]["weight"]
        fuelflow_moment_long = fuelflow[0]["moment_long"]
        config_moment_long = config_data["Weight"] * config_data["CG"]
    except KeyError:
        print("KeyError: check if 'weight','moment_long','CG' keys exist ")
        return config_data
    config_moment_long = config_data["Weight"] * config_data["CG"]
    centrogram = {
        "name": config_data["items"], "weight": [], "cg_long": []}
    config_moment_long = config_data["Weight"] * config_data["CG"]

    for weight, moment in list(zip(fuelflow_weight, fuelflow_moment_long)):
        # print(weight)
        centrogram["weight"].append(weight + config_data["Weight"])
        centrogram["cg_long"].append(
            ((moment + config_moment_long) /
                (weight + config_data["Weight"]))
        )
    # print(centrogram)
    return centrogram


def create_centrograms_from_configs(config, fuelflow):
    centrograms = []
    for tn_item in config:
        for derivative in tn_item["Derivatives"]:
            centrograms.append(add_config_to_fuelflow(fuelflow, derivative))
    return centrograms

def centrograms_builder(centrogram):
    centrograms=[]
    for j in range(len('weight')):
        centrograms.append([centrogram['weight'][j],centrogram['cg_long'][j]])
    return centrograms

# def envelope_from_query()
#     envjson=open("C:\Users\Gilad Timar\Documents\Tamnun\Tamnun\TamnunMainPage\DummyData\EnvelopeQuery1.json", 'r')
#     env_data=json.load(envjson)
#     envelope=[env_data["Weight"],env_data["CG"]]
#     return envelope
def filter_centrograms(centrograms, envelope):
    envelopes=[]
    limits=[]
    # print(len(envelope[0]))
    for i in range(len(envelope[0])):
        envelopes.append([envelope[0][i],envelope[1][i]])
    # centrograms=centrograms_builder(centrograms)
    # print(centrograms)
    # for j in range(len(centrogram['weight'])):
    #     centrograms.append(centrogram['weight'][j],centrogram['cg_long'][j])
    for dev in centrograms:
        centrogram=centrograms_builder(dev)
        print(centrogram)
        limits.append(LimitsFinder.fuel_limits_finder(envelopes, centrogram))
    # print(limits)
    return limits


def get_most_strict_limits(limits):
    # for limit in limits
    takeoff_limits = [limit[0] for limit in limits]
    landing_limits = [limit[-1] for limit in limits]

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
    # TODO: get data from server
    # TODO: calculatre for both long and lat

    
        #                                                      #
    # As of this point the code is writen for long SF without a DB #
        #                                                      #    

    # json data load
    datajson=open("C:/Users/Gilad Timar/Documents/Tamnun/Tamnun/TamnunMainPage/DummyData/platformQueryDataWBC1.json", 'r')
    platform=json.load(datajson)
    W_SF=platform["SF_W"]
    CG_SF=platform["SF_CGLong"]
    MAC=platform["MAC"]
    envjson=open("C:/Users/Gilad Timar/Documents/Tamnun/Tamnun/TamnunMainPage/DummyData/EnvelopeQueryWBC1.json", 'r')
    env_data=json.load(envjson)
    envelope=[env_data["envolopeData"]["Weight"],env_data["envolopeData"]["CG"]]
    ffjson=open("C:/Users/Gilad Timar/Documents/Tamnun/Tamnun/TamnunMainPage/DummyData/fuelFlowWBC1.json",'r')
    fuelflow=json.load(ffjson)
    # print(fuelflow[0]["weight"])
    
    
    # backend_calc_data =get_WB_calc_data(tms=parsed_client_request["TMS"])

    aircrafts = parsed_client_request["aircrafts"]
    for tail_num, weight, CGlong in zip(aircrafts[0]["Tail_num"], aircrafts[1]["Weight"], aircrafts[2]["CG"]):
        SF_aircrafts = apply_safety_factors(W_SF, CG_SF, weight, CGlong, tail_num, MAC=MAC)
    # parsed_client_request.pop("aircrafts")
    parsed_client_request["aircrafts"] = SF_aircrafts
    # print(parsed_client_request)

    discrete_configs = list_discrete_configs(parsed_client_request)
    # print(discrete_configs)
    # centrograms = create_centrograms_from_configs(discrete_configs, backend_calc_data["fuelFlows"])
    centrograms=create_centrograms_from_configs(discrete_configs,fuelflow)
    limits = filter_centrograms(centrograms,envelope)
    strict_limits = get_most_strict_limits(limits)
    ret = {
        "takeoff fuel": strict_limits[0],
        "landing fuel": strict_limits[1],
        "units": "קג",
        "centrogram": centrograms
    }
    return ret
# datajson=open("C:/Users/Gilad Timar/Documents/Tamnun/Tamnun/TamnunMainPage/DummyData/platformQueryData.json", 'r')
datajson=open("C:/Users/Gilad Timar/Documents/Tamnun/Tamnun/TamnunMainPage/DummyData/WBCalctest1.json", 'r')
WB=perform_WB_calc(json.load(datajson))
# print(WB)