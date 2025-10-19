import json
import urllib
from itertools import chain

from django.core.paginator import Paginator
from django.db.migrations import serializer
from django.shortcuts import render
from django.template.defaultfilters import title
from rest_framework import generics
from rest_framework.response import Response


from .documents import ElectroProductDocument, GasProductDocument, SantehProductDocument
from .forms import OrderForm
from .models import Rubric, Electro, Santeh, Gas, ElectroProduct, GasProduct, SantehProduct, Order, Feedback
from .serializers import OrderSerializer, FeedbackSerializer, ElectroSerializer, GasSerializer, \
    SantehSerializer
from .signals import get_cookies


# def get_basic(request):
#     rubrics = Rubric.objects.prefetch_related('electro_set', 'gas_set', 'santeh_set').all()
#     context = { 'rubrics': rubrics }
#     return render(request, 'basic.html', context)

def get_main_page(request):
    ''' Отдает данные на главную страницу. '''
    electro = Electro.objects.first()
    santeh = Santeh.objects.first()
    gas = Gas.objects.first()
    rubrics = Rubric.objects.prefetch_related('electro_set', 'gas_set', 'santeh_set').all()
    # Собираем все товары из всех категорий
    all_products = list(ElectroProduct.objects.all()) + \
                   list(GasProduct.objects.all()) + \
                   list(SantehProduct.objects.all())
    # Сортируем по дате добавления (по id, т.к. id растет с добавлением)
    all_products_sorted = sorted(all_products, key=lambda x: x.id, reverse=True)
    # Берем 5 последних
    latest_products = all_products_sorted[:6]
    popular_products = ElectroProduct.objects.all().order_by('id')[:6]
    context = {
        'electro': electro,
        'santeh': santeh,
        'gas': gas,
        'rubrics': rubrics,
        'latest_products': latest_products,
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
    electro_qs = ElectroProduct.objects.select_related('rubric').all()
    gas_qs = GasProduct.objects.select_related('rubric').all()
    santeh_qs = SantehProduct.objects.select_related('rubric').all()

    all_products = list(chain(electro_qs, gas_qs, santeh_qs))

    paginator = Paginator(all_products, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'rubrics':rubrics}
    return render(request, 'catalog.html', context)



def get_subrubrics(request, rubric_id):
    '''Список подразделов раздела '''
    rubric = Rubric.objects.get(pk=rubric_id)

    if rubric.rubric_name == 'Газовое оборудование':
        subrubrics = Gas.objects.select_related('rubric').all()
        products = GasProduct.objects.select_related('rubric').all()
    elif rubric.rubric_name == 'Электрика':
        subrubrics = Electro.objects.select_related('rubric').all()
        products = ElectroProduct.objects.select_related('rubric').all()
    elif rubric.rubric_name == 'Сантехника':
        subrubrics = Santeh.objects.select_related('rubric').all()
        products = SantehProduct.objects.select_related('rubric').all()

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


class SubrubricListAPIView(generics.ListAPIView):
    def get(self, request, **kwargs):
        data = {}
        data['subrubrics_electro'] =ElectroSerializer(Electro.objects.all(), many=True).data
        data['subrubrics_gas'] =GasSerializer(Gas.objects.all(), many=True).data
        data['subrubrics_santeh'] =SantehSerializer(Santeh.objects.all(), many=True).data
        return Response(data)



def get_products(request, rubric_id, subrubric_id):
    '''Выводит страницу оттдельного подраздела товары'''
    rubric = Rubric.objects.get(pk=rubric_id)
    if rubric.rubric_name == 'Газовое оборудование':
        products = GasProduct.objects.filter(rubric=subrubric_id)
        current_subrubric = Gas.objects.get(pk=subrubric_id)

    elif rubric.rubric_name == 'Электрика':
        products = ElectroProduct.objects.filter(rubric=subrubric_id)
        current_subrubric = Electro.objects.get(pk=subrubric_id)

    elif rubric.rubric_name == 'Сантехника':
        products = SantehProduct.objects.filter(rubric=subrubric_id)
        current_subrubric = Santeh.objects.get(pk=subrubric_id)

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

    if rubric.rubric_name == 'Газовое оборудование':
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
    context = {'form':form, 'rubrics': rubrics }
    return render(request, 'basket.html', context)


class OrderAPICreate(generics.CreateAPIView):
    '''Создает заказ.'''
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        raw_cookies = self.request.COOKIES.get('basket')
        decoded_cookies = urllib.parse.unquote(raw_cookies)
        basket_cookies = json.loads(decoded_cookies)
        order = serializer.save()
        get_cookies.send(sender=Order, instance=order, basket_cookies=basket_cookies )


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
    if not query:
        return render(request, 'search.html', {'results': [], 'message': 'Введите поисковый запрос'})

    results = []
    results += search_model_products(ElectroProductDocument, ElectroProduct, query)
    results += search_model_products(GasProductDocument, GasProduct, query)
    results += search_model_products(SantehProductDocument, SantehProduct, query)

    if not results:
        return render(request, 'search.html', {'results': [], 'message': 'Ничего не найдено'})

    return render(request, 'search.html', {'results': results})


class FeedbackAPICreate(generics.CreateAPIView):
    '''Создает запись обратной связи.'''
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer