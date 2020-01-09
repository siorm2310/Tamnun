from django.db import models
from django.contrib.postgres.fields import ArrayField,JSONField # Postgres specific fields

# Models file. contains the models for the Tamnun application. migrate these models to update the database

# TODO: Validate that all required parameters have been passed
# TODO: Choose a way for handling images and files (other then static files)
# TODO: Choose a way for handling sub - types of A/C

class AircraftType(models.Model):
    """
    Aircraft type describes the different platforms of the IAF, in TMS - resolution
    Sorted by TMS
    """
    RLE = models.FloatField(name='RLE')
    MAC = models.FloatField(null=True, name='MAC')
    TMS = models.CharField(max_length = 8, name = 'TMS', unique = True , help_text  = "Use the following format : XX-XX-XX") # AA-BB-CC format
    IAFname = models.CharField(max_length=32, name='IAFname' , help_text = "Hebrew name, e.g : Zik, Adir")
    modelName = models.CharField(max_length=32, name='modelName', help_text = "Commertial name, e.g : F-16, CH-53")
    # aircraftImage = models.ImageField(null = True)


    def __str__(self):
        return f"AIRCRAFT : {self.IAFname} ({self.modelName}) ; TMS : {self.TMS}"

class AircraftSubType(models.Model):
    """
    Aircraft sub type is, by its name, a sub category of an aircraft type.
    It describes differeces in the platform which are NOT seperated in TMS level.
    Examples of sub types : Zik TVUAA / DAF PLADA , EITAN MANA A / MANA B , YANSHUF 1/2/3
    """
    aircraftType = models.ForeignKey(AircraftType , on_delete=models.CASCADE)
    subTypeName = models.CharField(max_length=32)

    def __str__(self):
        return f"AIRCRAFT SUB TYPE : {self.subTypeName}"
        
class ItemGroup(models.Model):
    """
    ItemGroup model holds a unique identifier for items related to each other
    Items listed in the same item group are part of the same LRU or system 
    """

    itemGroupName = models.CharField(max_length=32 , name="itemGroupName")
    relatedAircraftType = models.ForeignKey(AircraftType, on_delete=models.CASCADE)
    relatedAircraftSubType = models.ForeignKey(AircraftSubType, on_delete=models.CASCADE)

    def __str__(self):
        return f"GROUP ITEM : {self.itemGroupName}"

class Item(models.Model):
    """
    Item model holds all items available for loading / unloading from an aircraft.
    allocated according to TMS
    """
    # TODO: Decide resolution of A/C division
    itemName = models.CharField(max_length=32, name='itemName')
    hasLateralData = models.BooleanField(name='hasLateralData')
    weight = models.FloatField(name='weight')
    x_cg = models.FloatField(name='x_cg')
    y_cg = models.FloatField(name='y_cg', null=True)
    relatedAircraft = models.ForeignKey(AircraftType, on_delete=models.CASCADE)
    itemGroup = models.ForeignKey(ItemGroup, on_delete=models.CASCADE, null=True)
    isFuelTank = models.BooleanField(name='isFuelTank')
    isExpendable = models.BooleanField(name='isExpendable')
    # itemImage = models.ImageField(null = True)

    def __str__(self):
        return f"ITEM : {self.itemName} ; WEIGHT = {self.weight} ; X-CG  = {self.x_cg} ; Y-CG = {self.y_cg}"

class Aircraft(models.Model):
    """
    Aircraft model holds the TN level of managment of aircrafts. Here are the TN basic data.
    """
    tailNumber = models.CharField(max_length=3, name='tailNumber')
    basicWeight = models.FloatField(name='basicWeight')
    basicXCG = models.FloatField(name='basicXCG')
    basicYCG = models.FloatField(name='basicYCG')
    aircraftType = models.ForeignKey(AircraftType, on_delete=models.CASCADE)
    aircraftSubType = models.ForeignKey(AircraftSubType, on_delete=models.CASCADE , null=True)

    def __str__(self):
        return f"AIRCRAFT TYPE : {self.aircraftType} ; TAIL NUMBER : {self.tailNumber} ; TMS : {AircraftType.TMS}"

class FuelFlow(models.Model):
    """
    FuelFlow model holds all fuel consumption data.
    Each fuelflow hold the relevant aircraft type, as well as the fuel tank which holds it.
    An aircraft type can be linked to multiple fuelflows
    WARNING : as we use the ArrayField database field, we need to use postgreSQL database
    """
    fuelFlowDescription = models.CharField(max_length = 32, name = 'fuelDescription')
    aircraftType = models.ForeignKey(AircraftType, on_delete=models.CASCADE )
    relatedItem = models.ForeignKey(Item, on_delete=models.CASCADE , null=True)
    isInternal = models.BooleanField()
    # fuelFlow = ArrayField(models.FloatField()) #TODO: choose design method for nX2 arrays
 
    def __str__(self):
        return f"FUEL-FLOW. AIRCRAFT TYPE : {self.aircraftType} ; DESCRIPTION : {self.fuelFlowDescription}"

class Envelopes(models.Model):
    """
    Envelopes model holds all weight-CG envelopes.
    Each Envelope holds the relevant aircraft type, as well as Longitudal/Lateral identifier.
    WARNING : as we use the ArrayField database field, we need to use postgreSQL database
    """
    ENVELOPE_TYPE = (('LONG','Longitudal'),('LAT', 'Lateral')) # Restrict choices for envelope types
    aircraftType = models.ForeignKey(AircraftType, on_delete=models.CASCADE , related_name='aircraftType')
    aircraftSubType = models.ForeignKey(AircraftSubType, on_delete=models.CASCADE, null=True)
    envelopeType = models.CharField(max_length=4, choices=ENVELOPE_TYPE, default='LONG')
    # Envelope = ArrayField(models.FloatField()) #TODO: choose design method for nX2 arrays

    def __str__(self):
        return f"ENVELOPE. AIRCRAFT TYPE : {self.aircraftType} ; TYPE : {self.envelopeType}"