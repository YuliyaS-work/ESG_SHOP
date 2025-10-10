from django.shortcuts import render

from .models import Rubric, Electro, Santeh, Gas, ElectroProduct, GasProduct, SantehProduct

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
    context = {
        'electro': electro,
        'santeh': santeh,
        'gas': gas,
        'rubrics': rubrics,
    }
    return render(request, 'main_page.html', context)



def get_catalog(request):
    '''Выводит разделы каталога и подразделы. '''
    rubrics = Rubric.objects.prefetch_related('electro_set', 'gas_set', 'santeh_set').all()
    # electro_subrubrics = Electro.objects.prefetch_related('electroproduct_set').all()
    # gas_subrubrics = Gas.objects.prefetch_related('gasproduct_set').all()
    # santeh_subrubrics = Santeh.objects.prefetch_related('santehproduct_set').all() #опечатка

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
    return render(request, 'reviews.html', context)

def get_partners(request):
    rubrics = Rubric.objects.all()
    context = {'rubrics': rubrics}
    return render(request, 'partners.html', context)


def get_basket(request):
    return render(request, 'basket.html')
