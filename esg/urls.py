from django.urls import path

from .views import OrderAPICreate
from .views import *

urlpatterns = [
    path('', get_main_page, name='main'),
    path('catalog/', get_catalog, name='catalog'),
    path('contacts/', get_contact, name='contacts'),
    path('payments/', get_payments, name='payments'),
    path('partners/', get_partners, name='partners'),
    path('privacy/', get_privacy, name='privacy'),

    path('basket/', get_basket, name='basket'),
    path('search/', search_view, name='search'),

    path('basket/api/order/', OrderAPICreate.as_view(), name='order_api_create'),
    path('api/feedback/', FeedbackAPICreate.as_view(), name='feedback'),

    path('<str:rubric_name_translit>/<int:subrubric_id>/<int:product_id>/', get_product, name='product'),
    path('<str:rubric_name_translit>/<int:subrubric_id>/', get_products, name='products'),
    path('<slug:rubric_name_translit>/', get_subrubrics, name='subrubrics'),




]
