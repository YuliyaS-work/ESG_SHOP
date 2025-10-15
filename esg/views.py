import json
import urllib

from django.db.migrations import serializer
from django.shortcuts import render
from django.template.defaultfilters import title
from rest_framework import generics

from .documents import ElectroProductDocument, GasProductDocument, SantehProductDocument
from .forms import OrderForm
from .models import Rubric, Electro, Santeh, Gas, ElectroProduct, GasProduct, SantehProduct, Order
from .serializers import OrderSerializer
from .signals import get_cookies

def get_basic(request):
    rubrics = Rubric.objects.prefetch_related('electro_set', 'gas_set', 'santeh_set').all()
    context = { 'rubrics': rubrics }
    return render(request, 'basic.html', context)

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
    latest_products = all_products_sorted[:5]
    popular_products = ElectroProduct.objects.all().order_by('id')[:5]
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
    '''Выводит разделы каталога и подразделы. '''
    #rubrics = Rubric.objects.prefetch_related('electro_set', 'gas_set', 'santeh_set').all()
    # electro_subrubrics = Electro.objects.prefetch_related('electroproduct_set').all()
    # gas_subrubrics = Gas.objects.prefetch_related('gasproduct_set').all()
    # santeh_subrubrics = Santeh.objects.prefetch_related('santehproduct_set').all() #опечатка
    rubrics = Rubric.objects.prefetch_related(
        'electro_set__electroproduct_set',
        'gas_set__gasproduct_set',
        'santeh_set__santehproduct_set'
    ).all()
    context = {
        'rubrics': rubrics,
    }
    return render(request, 'catalog.html', context)


def get_subrubrics(request, rubric_id):
    '''Список подразделов раздела '''
    rubric = Rubric.objects.get(pk=rubric_id)

    if rubric.rubric_name == 'Газовое оборудование':
        subrubrics = Gas.objects.all()
    elif rubric.rubric_name == 'Электрика':
        subrubrics = Electro.objects.all()
    elif rubric.rubric_name == 'Сантехника':
        subrubrics = Santeh.objects.all()

    # Получаем все рубрики для сайдбара
    rubrics = Rubric.objects.all()

    context = {'subrubrics': subrubrics, 'rubric': rubric, 'rubrics': rubrics}
    return render(request, 'subrubrics_list.html', context)


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

    # Получаем все рубрики для сайдбара
    rubrics = Rubric.objects.all()

    context = {
        'products':products,
        'current_subrubric':current_subrubric,
        'rubrics': rubrics
    }
    return render(request, 'products_list.html', context)



def get_product(request, rubric_id, subrubric_id, product_id):
    rubric = Rubric.objects.get(pk=rubric_id)

    if rubric.rubric_name == 'Газовое оборудование':
        product = GasProduct.objects.get(pk=product_id)
    elif rubric.rubric_name == 'Сантехника':
        product = SantehProduct.objects.get(pk=product_id)
    elif rubric.rubric_name == 'Электрика':
        product = ElectroProduct.objects.get(pk=product_id)

    # Получаем все рубрики для сайдбара
    rubrics = Rubric.objects.all()

    context = {'product':product, 'rubrics': rubrics}
    return render(request, 'product.html', context)


def get_contact(request):
    rubrics = Rubric.objects.all()
    context = {'rubrics': rubrics}
    return render(request, 'contact.html', context)

def get_payments(request):
    rubrics = Rubric.objects.all()
    context = {'rubrics': rubrics}
    return render(request, 'payments.html', context)

def get_reviews(request):
    rubrics = Rubric.objects.all()
    context = {'rubrics': rubrics}
    return render(request, 'contact-form.html', context)

def get_partners(request):
    rubrics = Rubric.objects.all()
    context = {'rubrics': rubrics}
    return render(request, 'partners.html', context)


def get_basket(request):
    form = OrderForm()
    rubrics = Rubric.objects.all()
    context = {'form':form, 'rubrics': rubrics }
    return render(request, 'basket.html', context)


class OrderAPICreate(generics.CreateAPIView):
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


