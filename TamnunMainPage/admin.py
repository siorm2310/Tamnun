from django.contrib import admin

from .models import *
# Register your models here.
# The models listed here will appear on the admin page for easy addition and changes

admin.site.register(AircraftType)
admin.site.register(Aircraft)
admin.site.register(Item)
admin.site.register(FuelFlow)
admin.site.register(Envelopes)
