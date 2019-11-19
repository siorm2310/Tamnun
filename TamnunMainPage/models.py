from django.db import models

# Create your models here.

class Aircraft(models.Model):
    RLE = models.FloatField(name='RLE')
    MAC = models.FloatField(null=True, name='MAC')
    TMS = models.IntegerField(max_length=6, name='TMS', unique=True)
    IAFname = models.CharField(max_length=32, name='IAFname')
    modelName = models.CharField(max_length=32, name='modelName')
    
    def __str__(self):
        return f"AIRCRAFT {self.IAFname} ({self.modelName}) ; TMS : {self.TMS}"

class Item(models.Model):
    itemName = models.CharField(max_length=32, name='itemName')
    hasLateralData = models.BooleanField(name='hasLateralData')
    weight = models.FloatField(name='weight')
    x_cg = models.FloatField(name='x_cg')
    y_cg = models.FloatField(name='y_cg')
    # TODO : add is lateral option
    
    def __str__(self):
        return f"ITEM : {self.itemName} ; WEIGHT = {self.weight} ; X-CG  = {self.x_cg} ; Y-CG = {self.y_cg}"

class TailNumber(models.Model):
    pass