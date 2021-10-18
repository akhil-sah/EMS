from django.contrib import admin
from . models import * 
# Register your models here.

admin.site.register(Person)
admin.site.register(Phone_no)
admin.site.register(Complaints)
admin.site.register(Emission_parameters)
admin.site.register(Survey_metadata)
admin.site.register(Survey_data)
admin.site.register(Session)
admin.site.register(Company_emissions)

