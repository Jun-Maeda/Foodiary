from django.contrib import admin
from .models import Area, Place, Shop, Food, FeelLog, Food_menu

# 場所でリレーションしているものを表示
class PlaceInline(admin.StackedInline):
    model = Place
    extra = 0

# お店でリレーションしているものを表示
class ShopInline(admin.StackedInline):
    model = Shop
    extra = 0

# 記録でリレーションしているものを表示
class FeelLogInline(admin.StackedInline):
    model = FeelLog
    extra = 0

class AreaAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [PlaceInline]


class PlaceAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [ShopInline]


class ShopAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [FeelLogInline]


class FoodAdmin(admin.ModelAdmin):
    list_display = ['name']


class FeelLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'evaluation']


admin.site.register(Area, AreaAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(FeelLog, FeelLogAdmin)
admin.site.register(Food_menu)
