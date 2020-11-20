from django.contrib import admin
from .models import Order, Orderer, Profile, TypeWork, Vipovilny, Rayon, Kadastr_Number, Rozrobnik, Doverenost, Oblast, Otg


# Register your models here.
@admin.register(Kadastr_Number)
class KadastrNumberAdmin(admin.ModelAdmin):
    list_display = ('kadastr_number',  'razbivka', 'who_added', 'who_edit')


admin.site.register(Order)
admin.site.register(Orderer)
admin.site.register(Profile)
admin.site.register(TypeWork)
admin.site.register(Vipovilny)
admin.site.register(Rayon)
admin.site.register(Rozrobnik)
admin.site.register(Doverenost)
admin.site.register(Oblast)
admin.site.register(Otg)

