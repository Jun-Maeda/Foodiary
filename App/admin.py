from django.contrib import admin
from .models import Area, Place, Shop, Food, FeelLog


class AreaAdmin(admin.ModelAdmin):
    list_display = ['name']

class PlaceAdmin(admin.ModelAdmin):
    list_display = ['name']

class ShopAdmin(admin.ModelAdmin):
    list_display = ['name']

class FoodAdmin(admin.ModelAdmin):
    list_display = ['name']

class FeelLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'list', 'date']

admin.site.register(Area, AreaAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(FeelLog, FeelLogAdmin)
