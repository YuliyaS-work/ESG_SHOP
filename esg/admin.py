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
    search_fields = ('title','rubric__title')

class GasProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'rubric', 'photo', 'price')
    ordering = ('title',)
    search_fields = ('title','rubric__title')

class SantehProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'rubric', 'photo', 'price')
    ordering = ('title',)
    search_fields = ('title','rubric__title')

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id','status',
        'first_name',
        'last_name',
        'phone',
        'date',
        'get_gasproducts',
        'get_electroproducts',
        'get_santehproducts'
    )
    ordering = ('-date',)
    search_fields = ('last_name', 'date', 'phone', 'status')

    def get_gasproducts(self, obj):
        dict_order = {}
        for product in obj.gasproduct_set.all():
            gasorder = obj.gasorder_set.filter(gasproduct_id=product.pk).first()
            dict_order[product.title] = f'{gasorder.quantity} (шт./м)'
        return dict_order
    get_gasproducts.short_description = 'Газовое оборудование'

    def get_electroproducts(self, obj):
        dict_order = {}
        for product in obj.electroproduct_set.all():
            electroorder = obj.electroorder_set.filter(electroproduct_id=product.pk).first()
            dict_order[product.title] = f'{electroorder.quantity} (шт./м)'
        return dict_order
    get_electroproducts.short_description = 'Электрика'

    def get_santehproducts(self, obj):
        dict_order = {}
        for product in obj.santehproduct_set.all():
            santehorder = obj.santehorder_set.filter(santehproduct_id=product.pk).first()
            dict_order[product.title] = f'{santehorder.quantity} (шт./м)'
        return dict_order
    get_santehproducts.short_description = 'Сантехника'


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('date', 'name', 'phone', 'subject', 'message', 'status')
    ordering = ('-date',)
    search_fields = ('phone', 'date', 'name')


admin.site.register(Electro, ElectroAdmin)
admin.site.register(Gas, GasAdmin)
admin.site.register(Santeh, SantehAdmin)
admin.site.register(GasProduct, GasProductAdmin)
admin.site.register(ElectroProduct, GasProductAdmin)
admin.site.register(SantehProduct, SantehProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Feedback, FeedbackAdmin)

