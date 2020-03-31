from django.db import models
from django.contrib.postgres.fields import ArrayField,JSONField # Postgres specific fields
from django.core.validators import RegexValidator
# Models file. contains the models for the Tamnun application. migrate these models to update the database

# TODO: Validate that all required parameters have been passed
# TODO: Choose a way for handling images and files (other than static files)
# TODO: create functionality for delivering data to front end

class AircraftType(models.Model):
    """
    Aircraft type describes the different platforms of the IAF, in TMS - resolution
    Sorted by TMS
    """
    RLE = models.FloatField(name='RLE')
    MAC = models.FloatField(name='MAC',null=True , blank=True)
    TMS = models.CharField(max_length = 8, name = 'TMS', unique = True, 
    help_text  = "Use the following format : XX-XX-XX",validators = [RegexValidator(r"^\d{2}-\d{2}-\d{2}$", )]) # AA-BB-CC format
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
    relatedAircraftType = models.ForeignKey(AircraftType , on_delete=models.CASCADE)
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
    itemName = models.CharField(max_length=32, name='Item mame')
    hasLateralData = models.BooleanField(name='Item has lateral data?')
    weight = models.FloatField(name='Weight')
    weight_delta = models.FloatField(name='weight delta', default=0, help_text="Does the item has weight derivative data?")
    x_cg = models.FloatField(name='x_cg')
    y_cg = models.FloatField(name='y_cg', blank=True)
    x_dim = models.FloatField(name='x_dim', default=10, help_text="Enter estimated dimentions relative to A/C in inch/cm. If not known, set to default") # X dimentions for the item
    y_dim = models.FloatField(name='y_dim', default=10, help_text="Enter estimated dimentions relative to A/C in inch/cm. If not known, set to default") # Y dimentions for the item
    relatedAircraftType = models.ForeignKey(AircraftType, on_delete=models.CASCADE)
    itemGroup = models.ForeignKey(ItemGroup, on_delete=models.CASCADE, null=True , blank=True)
    # itemImage = models.ImagLeField(null = True) 

    def __str__(self):
        return f"ITEM : {self.itemName} ; A/C : {self.relatedAircraftType}"

class MunitionAndExternals(Item):
    parentItem = models.ForeignKey('self', on_delete=models.CASCADE) # parent Item (chain of munition loading) is within MunitionAndExternals category
    

class FuelTank(Item):
    pass

class Aircraft(models.Model):
    """
    Aircraft model holds the TN level of managment of aircrafts. Here are the TN basic data.
    """
    tailNumber = models.CharField(max_length=3, name='tailNumber')
    basicWeight = models.FloatField(name='basicWeight')
    basicXCG = models.FloatField(name='basicXCG')
    basicYCG = models.FloatField(name='basicYCG')
    relatedAircraftType = models.ForeignKey(AircraftType, on_delete=models.CASCADE)
    relatedAircraftSubType = models.ForeignKey(AircraftSubType, on_delete=models.CASCADE , null=True)

    def __str__(self):
        return f"TAIL NUMBER : {self.tailNumber} TYPE : {self.relatedAircraftType} SUB_TYPE : {self.aircraftSubType}"

class FuelFlow(models.Model):
    """
    FuelFlow model holds all fuel consumption data.
    Each fuelflow hold the relevant aircraft type, as well as the fuel tank which holds it.
    An aircraft type can be linked to multiple fuelflows
    WARNING : as we use the ArrayField database field, we need to use postgreSQL database
    """
    fuelFlowDescription = models.CharField(max_length = 32, name = 'fuelDescription',  help_text="Enter a short description for the fuel flow")
    relatedAircraftType = models.ForeignKey(AircraftType, on_delete=models.CASCADE)
    relatedItem = models.ForeignKey(Item, on_delete=models.CASCADE , null=True , blank=True)
    isInternal = models.BooleanField()
    fuelFlow = ArrayField(ArrayField(models.FloatField()), default=list)
 
    def __str__(self):
        return f"FUEL-FLOW. AIRCRAFT TYPE : {self.relatedAircraft} ; DESCRIPTION : {self.fuelFlowDescription}"

class Envelope(models.Model):
    """
    Envelopes model holds all weight-CG envelopes.
    Each Envelope holds the relevant aircraft type, as well as Longitudal/Lateral identifier.
    WARNING : as we use the ArrayField database field, we need to use postgreSQL database
    """
    envelopeName = models.CharField(max_length=32 , help_text="Enter a short description for the envelope" , default = "")
    ENVELOPE_TYPE = (('LONG','Longitudal'),('LAT', 'Lateral')) # Restrict choices for envelope types
    relatedAircraftType = models.ForeignKey(AircraftType, on_delete=models.CASCADE , related_name='aircraftType')
    relatedAircraftSubType = models.ForeignKey(AircraftSubType, on_delete=models.CASCADE, null=True , blank=True)
    envelopeType = models.CharField(max_length=4, choices=ENVELOPE_TYPE, default='LONG')
    Envelope = ArrayField(ArrayField(models.FloatField()))

    def __str__(self):
        return f"ENVELOPE. AIRCRAFT TYPE : {self.relatedAircraftType} ; TYPE : {self.envelopeType}"