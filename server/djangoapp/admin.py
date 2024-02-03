from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel

# Register your models here.
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1

# CarModelInline class
class CarModelAdmin(admin.ModelAdmin):
    fields = ['name', 'type', "make", 'id']
    list_display = ('name', 'make', 'type')

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ['name', 'type', "make", 'id']
    list_display = ('name', 'make', 'type')

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ('name', 'description')

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)