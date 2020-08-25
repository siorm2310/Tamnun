from .models import *
import json
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, get_list_or_404


class ViewQueries:
    @staticmethod
    def get_frontend_data(tms):
        """Get relevant data to display in the UI

        Arguments:
            tms {string} -- TMS string of chosen aircraft
        Returns:
            data [dict] -- dictionary holding the data extracted from DB
        """
        try:
            aircraftType = AircraftType.objects.get(TMS=tms)
            aircrafts = Aircraft.objects.filter(
                relatedAircraftType=aircraftType
            ).values()
            items = Item.objects.filter(
                relatedAircraftType=aircraftType).values()
            fuelFlows = FuelFlow.objects.filter(
                relatedAircraftType=aircraftType
            ).values()
            envelopes = Envelope.objects.filter(
                relatedAircraftType=aircraftType
            ).values()

            data = {
                "aircraftType": aircraftType.IAFname,
                "aircrafts": list(aircrafts),
                "items": list(items),
                "fuelFlows": list(fuelFlows),
                "envelopes": list(envelopes),
            }
        except ObjectDoesNotExist as err:
            print(err)
            data = {}
        return data


class WBQueries:
    @staticmethod
    def get_WB_calc_data(tms):
        aircraftType = get_object_or_404(AircraftType, TMS=tms)
        try:
            fuelFlows = FuelFlow.objects.filter(relatedAircraftType=aircraftType).values()
            envelopes = Envelope.objects.filter(relatedAircraftType=aircraftType).values()
        except:
            print("Error retirieving fuelflows and envelopes")

        data = {
            "aircraftType": aircraftType,
            "fuelFlows": list(fuelFlows),
            "envelopes": list(envelopes),
        }

        return data
