from django.contrib import admin
from models import City, Country, State

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_2', 'iso_3', 'continent', 'currency')


admin.site.register(City)
admin.site.register(State)
admin.site.register(Country, CountryAdmin)

