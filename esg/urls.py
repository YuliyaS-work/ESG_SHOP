from django.urls import path

from .views import *

urlpatterns = [
    path('', get_main_page, name='main'),
    path('catalog/', get_catalog, name='catalog'),
    path('catalog/gas<int:rubric_id>/', get_rubric_gas, name='rubric_gas'),
    path('catalog/electro<int:rubric_id>/', get_rubric_electro, name='rubric_electro'),
    path('catalog/santeh<int:rubric_id>/', get_rubric_santeh, name='rubric_santeh'),
    path('catalog/gas<int:rubric_id>/<int:gasproduct_id>/', get_product_gas, name='product_gas'),
    path('catalog/electro<int:rubric_id>/<int:electroproduct_id>/', get_product_electro, name='product_electro'),
    path('catalog/santeh<int:rubric_id>/<int:santehproduct_id>/', get_product_santeh, name='product_santeh'),
]
