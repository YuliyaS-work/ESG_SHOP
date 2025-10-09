from django.urls import path

from .views import *

urlpatterns = [
    path('', get_main_page, name='main'),
    path('catalog/', get_catalog, name='catalog'),
    path('catalog/<int:rubric_id>', get_subrubrics, name='subrubrics'),
    path('catalog/<int:rubric_id>/<int:subrubric_id>/', get_products, name='products'),
    path('catalog/<int:rubric_id>/<int:subrubric_id>/<int:product_id>', get_product, name='product'),

]
handler404 = 'esg.views.custom_404'