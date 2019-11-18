from django.db import models

# Create your models here.

class Aircraft(models.Model):
    RLE = models.FloatField(name='RLE')
    MAC = models.FloatField(null=True, name='MAC')
    TMS = models.IntegerField(max_length=6, name='TMS', unique=True)
    IAFname = models.CharField(max_length=32, name='IAFname')
    modelName = models.CharField(max_length=32, name='modelName')
    
    def __str__(self):
        return f"AIRCRAFT {self.IAFname} ({self.modelName}), TMS : {self.TMS}"

class Item(models.Model):
    pass

class TailNumber(models.Model):
    pass