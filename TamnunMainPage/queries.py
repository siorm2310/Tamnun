from .models import *
import json
from django.core.exceptions import ObjectDoesNotExist

class ViewQueries():

    @staticmethod
    def get_frontend_data(tms):
        """Get relevant data to display in the UI
        
        Arguments:
            tms {string} -- TMS string of chosen aircraft
        
        Returns:
            data [dict] -- dictionary holding the data extracted from DB
        """
        try:
            aircraftType = AircraftType.objects.get(TMS = tms)
            aircrafts = Aircraft.objects.filter(relatedAircraftType = aircraftType).values()
            items = Item.objects.filter(relatedAircraftType = aircraftType).values()
            fuelFlows = FuelFlow.objects.filter(relatedAircraftType = aircraftType).values()
            envelopes = Envelope.objects.filter(relatedAircraftType = aircraftType).values()
        
            data = {
                "aircraftType" : aircraftType.IAFname,
                "aircrafts" : list(aircrafts),
                "items" : list(items),
                "fuelFlows" : list(fuelFlows),
                "envelopes" : list(envelopes)
            }  
        except ObjectDoesNotExist as err:
            print(err)
            data = {}
        return data