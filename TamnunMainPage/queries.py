from .models import *
import json
class ViewQueries():

    @staticmethod
    def get_frontend_data(tms):
        try:
            aircraftType = AircraftType.objects.get(TMS = tms)
            aircrafts = Aircraft.objects.filter(relatedAircraft = aircraftType).get()
            items = Item.objects.filter(relatedAircraft = aircraftType).get()
            fuelFlows = FuelFlow.objects.filter(aircraftType = aircraftType).get()
            envelopes = Envelope.objects.filter(aircraftType = aircraftType).get()
        
            data = {
                "aircraftType" : aircraftType,
                "aircrafts" : aircrafts,
                "items" : items,
                "fuelFlows" : fuelFlows,
                "envelopes" : envelopes
            }  
        except:
            data = {} 
        return data