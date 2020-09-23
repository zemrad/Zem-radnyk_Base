from django.contrib import admin
from .models import Order, Orderer, Profile, TypeWork, Vipovilny, Rayon, Kadastr_Number, Rozrobnik

# Register your models here.

admin.site.register(Order)
admin.site.register(Orderer)
admin.site.register(Profile)
admin.site.register(TypeWork)
admin.site.register(Vipovilny)
admin.site.register(Rayon)
admin.site.register(Rozrobnik)
admin.site.register(Kadastr_Number)
