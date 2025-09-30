from django.contrib import admin

from .models import *

admin.site.register(Rubric)


class ElectroAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ('title',)
    search_fields = ('title',)

class GasAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ('title',)
    search_fields = ('title',)

class SantehAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ('title',)
    search_fields = ('title',)

class ElectroProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'rubric', 'photo', 'price')
    ordering = ('title',)
    search_fields = ('title','rubric_title')

class GasProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'rubric', 'photo', 'price')
    ordering = ('title',)
    search_fields = ('title','rubric__title')

class SantehProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'rubric', 'photo', 'price')
    ordering = ('title',)
    search_fields = ('title','rubric__title')

admin.site.register(Electro, ElectroAdmin)
admin.site.register(Gas, GasAdmin)
admin.site.register(Santeh, SantehAdmin)
admin.site.register(GasProduct, GasProductAdmin)
admin.site.register(ElectroProduct, GasProductAdmin)
admin.site.register(SantehProduct, SantehProductAdmin)

