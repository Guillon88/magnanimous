from django.contrib.gis.admin import OSMGeoAdmin
#from leaflet.admin import LeafletGeoAdmin
from django.contrib import admin

from .models import Item

#admin.site.register(Item, LeafletGeoAdmin)

@admin.register(Item)
class EventoAdmin(OSMGeoAdmin):
    list_display = ('fecha', 'tipo')