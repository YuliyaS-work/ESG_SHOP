from django.urls import path

from .views import OrderAPICreate
from .views import *

urlpatterns = [
    path('', get_main_page, name='main'),
    path('catalog/', get_catalog, name='catalog'),
    path('catalog/<int:rubric_id>', get_subrubrics, name='subrubrics'),
    path('catalog/<int:rubric_id>/<int:subrubric_id>/', get_products, name='products'),
    path('catalog/<int:rubric_id>/<int:subrubric_id>/<int:product_id>', get_product, name='product'),
    path('contacts/', get_contact, name='contacts'),
    path('payments/', get_payments, name='payments'),
    path('partners/', get_partners, name='partners'),

    path('basket/', get_basket, name='basket'),
    path('search/', search_view, name='search'),

    path('basket/api/order/', OrderAPICreate.as_view(), name='order_api_create'),
    path('api/feedback/', FeedbackAPICreate.as_view(), name='feedback'),

]
