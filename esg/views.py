import json
import urllib
from itertools import chain

from django.core.paginator import Paginator
from django.db.migrations import serializer
from django.db.models.functions import Lower
from django.shortcuts import render
from django.template.defaultfilters import title
from rest_framework import generics
from rest_framework.response import Response


from .documents import ElectroProductDocument, GasProductDocument, SantehProductDocument
from .forms import OrderForm
from .models import Rubric, Electro, Santeh, Gas, ElectroProduct, GasProduct, SantehProduct, Order, Feedback
from .serializers import OrderSerializer, FeedbackSerializer
# from .signals import get_cookies
from .tasks.email_order import process_order_task
from .tasks.email_feedback import process_feedback_task

def get_popular_products():
    '''Выводит популярные товары по усмотрению продавца. '''
    electro_products = ElectroProduct.objects.filter(status_popular=True)
    gas_products = GasProduct.objects.filter(status_popular=True)
    santeh_products = SantehProduct.objects.filter(status_popular=True)
    popular_products = list(chain(electro_products, gas_products, santeh_products))
    return popular_products


def get_new_products():
    '''Выводит новикнки товары по усмотрению продавца. '''
    # Выводит популярные товары по усмотрению продавца.
    electro_products = ElectroProduct.objects.filter(status_new=True)
    gas_products = GasProduct.objects.filter(status_new=True)
    santeh_products = SantehProduct.objects.filter(status_new=True)
    new_products = list(chain(electro_products, gas_products, santeh_products))
    return new_products


def get_main_page(request):
    ''' Отдает данные на главную страницу. '''
    electro = Electro.objects.first()
    santeh = Santeh.objects.first()
    gas = Gas.objects.first()
    rubrics = Rubric.objects.prefetch_related('electro_set', 'gas_set', 'santeh_set').all()

    popular_products = get_popular_products()
    new_products = get_new_products()

    context = {
        'electro': electro,
        'santeh': santeh,
        'gas': gas,
        'rubrics': rubrics,
        'new_products': new_products,
        'popular_products': popular_products,
    }
    return render(request, 'main_page.html', context)

def get_catalog(request):
    '''Выводит разделы каталога и подразделы (+js), выводит все товары, пагинация страницы по товарам.'''

    rubrics = Rubric.objects.prefetch_related(
            'electro_set__electroproduct_set',
            'gas_set__gasproduct_set',
            'santeh_set__santehproduct_set'
    ).all()
    electro_qs = ElectroProduct.objects.select_related('rubric', 'rubric__rubric').all()
    gas_qs = GasProduct.objects.select_related('rubric', 'rubric__rubric').all()
    santeh_qs = SantehProduct.objects.select_related('rubric', 'rubric__rubric').all()

    all_products = list(chain(electro_qs, gas_qs, santeh_qs))

    # фильтр
    sort = request.GET.get('sort', '')
    if sort == 'price_asc':
        all_products = sorted(all_products, key=lambda obj: obj.price)
    elif sort == 'price_desc':
        all_products = sorted(all_products, key=lambda obj: obj.price, reverse=True)
    elif sort == 'title_asc':
        all_products = sorted(all_products, key=lambda obj: obj.title.lower())
    elif sort == 'title_desc':
        all_products = sorted(all_products, key=lambda obj: obj.title.lower(), reverse=True)
    elif sort == 'popular':
        all_products = sorted(all_products, key=lambda obj: obj.counter, reverse=True)


    paginator = Paginator(all_products, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'rubrics':rubrics}
    return render(request, 'catalog.html', context)



def get_subrubrics(request, rubric_id):
    '''Список подразделов раздела '''
    rubric = Rubric.objects.get(pk=rubric_id)

    if rubric.rubric_name == 'Газификация':
        subrubrics = Gas.objects.select_related('rubric').all()
        products = GasProduct.objects.select_related('rubric').all()
    elif rubric.rubric_name == 'Электрика':
        subrubrics = Electro.objects.select_related('rubric').all()
        products = ElectroProduct.objects.select_related('rubric').all()
    elif rubric.rubric_name == 'Сантехника':
        subrubrics = Santeh.objects.select_related('rubric').all()
        products = SantehProduct.objects.select_related('rubric').all()

    # фильтр
    sort = request.GET.get('sort', '')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'title_asc':
        products = products.annotate(lower_title=Lower('title')).order_by('lower_title')
    elif sort == 'title_desc':
        products = products.annotate(lower_title=Lower('title')).order_by('-lower_title')
    elif sort == 'popular':
        products = products.order_by('-counter')

    paginator = Paginator(products, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Получаем все рубрики для сайдбара
    rubrics = Rubric.objects.prefetch_related('electro_set', 'gas_set', 'santeh_set').all()

    context = {
        'subrubrics': subrubrics,
        'rubrics': rubrics,
        'page_obj': page_obj,
    }
    return render(request, 'subrubrics_list.html', context)


def get_products(request, rubric_id, subrubric_id):
    '''Выводит страницу оттдельного подраздела товары'''
    rubric = Rubric.objects.get(pk=rubric_id)

    if rubric.rubric_name == 'Газификация':
        products = GasProduct.objects.filter(rubric=subrubric_id)
        current_subrubric = Gas.objects.get(pk=subrubric_id)

    elif rubric.rubric_name == 'Электрика':
        products = ElectroProduct.objects.filter(rubric=subrubric_id)
        current_subrubric = Electro.objects.get(pk=subrubric_id)

    elif rubric.rubric_name == 'Сантехника':
        products = SantehProduct.objects.filter(rubric=subrubric_id)
        current_subrubric = Santeh.objects.get(pk=subrubric_id)

    # фильтр
    sort = request.GET.get('sort', '')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'title_asc':
        products = products.annotate(lower_title=Lower('title')).order_by('lower_title')
    elif sort == 'title_desc':
        products = products.annotate(lower_title=Lower('title')).order_by('-lower_title')
    elif sort == 'popular':
        products = products.order_by('-counter')

    paginator = Paginator(products, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Получаем все рубрики для сайдбара
    rubrics = Rubric.objects.prefetch_related('electro_set', 'gas_set', 'santeh_set').all()

    context = {
        'rubrics': rubrics,
        'page_obj': page_obj,
        'current_subrubric': current_subrubric
    }
    return render(request, 'products_list.html', context)



def get_product(request, rubric_id, subrubric_id, product_id):
    '''Рендерит страницу одного продукта.'''
    rubric = Rubric.objects.get(pk=rubric_id)

    if rubric.rubric_name == 'Газификация':
        product = GasProduct.objects.get(pk=product_id)
    elif rubric.rubric_name == 'Сантехника':
        product = SantehProduct.objects.get(pk=product_id)
    elif rubric.rubric_name == 'Электрика':
        product = ElectroProduct.objects.get(pk=product_id)

    # Получаем все рубрики для сайдбара
    rubrics = Rubric.objects.prefetch_related('electro_set', 'gas_set', 'santeh_set').all()

    context = {'product':product, 'rubrics': rubrics}
    return render(request, 'product.html', context)


def get_contact(request):
    '''Рендерит страницу контактов.'''
    rubrics = Rubric.objects.prefetch_related('electro_set', 'gas_set', 'santeh_set').all()
    context = {'rubrics': rubrics}
    return render(request, 'contact.html', context)

def get_payments(request):
    '''Рендерит страницу оплаты и доставки'''
    rubrics = Rubric.objects.prefetch_related('electro_set', 'gas_set', 'santeh_set').all()
    context = {'rubrics': rubrics}
    return render(request, 'payments.html', context)

def get_partners(request):
    '''Рендерит страницу деловых партнеров'''
    rubrics = Rubric.objects.prefetch_related('electro_set', 'gas_set', 'santeh_set').all()
    context = {'rubrics': rubrics}
    return render(request, 'partners.html', context)


def get_basket(request):
    '''Рендерит страницу покупательской корзины.'''
    form = OrderForm()
    rubrics = Rubric.objects.prefetch_related('electro_set', 'gas_set', 'santeh_set').all()
    recently_products = ElectroProduct.objects.all()[:7] #переделать
    popular_products = get_popular_products()
    context = {'form':form, 'rubrics': rubrics, 'popular_products': popular_products, 'recently_products': recently_products}
    return render(request, 'basket.html', context)


def search_model_products(document_class, model_class, query):
    '''Используется для search_view, для вызова внутри'''
    results = []
    search = document_class.search().query(
        "multi_match",
        query=query,
        fields=['title', 'description'],
        fuzziness="AUTO"
    )
    try:
        response = search.execute()
        for hit in response:
            item = {
                'title': hit.title,
                'description': hit.description
            }

            product = model_class.objects.filter(title=hit.title).first()
            if product:
                item['product_id'] = product.pk
                item['subrubric_id'] = product.rubric.pk
                item['rubric_id'] = product.rubric.rubric.pk

            results.append(item)
    except Exception as e:
        print(f"Ошибка при поиске {model_class.__name__}: {e}")

    return results


def search_view(request):
    '''Посуществляет поиск товаров по сайту. '''
    query = request.GET.get('q', '')

    # Получаем рубрики для sidebar
    rubrics = Rubric.objects.prefetch_related('electro_set', 'gas_set', 'santeh_set').all()
    context = {'rubrics': rubrics}
    if not query:
        return render(request, 'search.html', {'results': [], 'message': 'Введите поисковый запрос'})

    results = []
    results += search_model_products(ElectroProductDocument, ElectroProduct, query)
    results += search_model_products(GasProductDocument, GasProduct, query)
    results += search_model_products(SantehProductDocument, SantehProduct, query)

    if not results:
        context.update({'results': [], 'message': 'Ничего не найдено'})
        return render(request, 'search.html', context)
    context.update({'results': results})
    return render(request, 'search.html', context)


class OrderAPICreate(generics.CreateAPIView):
    '''Создает заказ.'''
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        raw_basket = self.request.COOKIES.get('basket')
        decoded_basket_cookies = urllib.parse.unquote(raw_basket)
        basket_cookies = json.loads(decoded_basket_cookies)
        print(basket_cookies)

        order = serializer.save()
        # get_cookies.send(sender=Order, instance=order, basket_cookies=basket_cookies )
        process_order_task.delay(order_id=order.pk, basket_cookies=basket_cookies)


class FeedbackAPICreate(generics.CreateAPIView):
    '''Создает запись обратной связи.'''
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def perform_create(self, serializer):
        feedback = serializer.save()
        process_feedback_task.delay(feedback_id=feedback.pk)




