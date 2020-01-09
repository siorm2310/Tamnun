from django.contrib import admin

from .models import Aircraft,AircraftType,Item,FuelFlow,Envelopes
# Register your models here.
# The models listed here will appear on the admin page for easy addition and changes

admin.site.register(AircraftType)
# admin.site.register(AircraftSubType)
admin.site.register(Aircraft)
# admin.site.register(GroupItem)
admin.site.register(Item)
admin.site.register(FuelFlow)
admin.site.register(Envelopes)