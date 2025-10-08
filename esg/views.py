from django.shortcuts import render

from .models import *


def get_main_page(request):
    ''' Отдает данные на главную страницу. '''
    pass
    return render(request, 'main_page.html')


def get_catalog(request):
    '''Выводит разделы каталога и подразделы. '''
    rubrics = Rubric.objects.prefetch_related('electro_set', 'gas_set', 'santeh_set').all()
    # electro_subrubrics = Electro.objects.prefetch_related('electroproduct_set').all()
    # gas_subrubrics = Gas.objects.prefetch_related('gasproduct_set').all()
    # santeh_subrubrics = Electro.objects.prefetch_related('santehproduct_set').all()

    context = {
        'rubrics': rubrics,
        # 'electro_subrubrics': electro_subrubrics,
        # 'gas_subrubrics': gas_subrubrics,
        # 'santeh_subrubrics': santeh_subrubrics
    }

    return render(request, 'catalog.html', context)

def get_rubric_gas(request, rubric_id):
    '''Выводит страницу оттдельного подраздела газового оборудования'''
    products = GasProduct.objects.filter(rubric=rubric_id)
    gas = Gas.objects.all()
    current_rubric = Gas.objects.get(pk=rubric_id)
    context = {
        'products':products,
        'gas':gas,
        'current_rubric':current_rubric
    }
    return render(request, 'products_list.html', context)

def get_rubric_electro(request, rubric_id):
    '''Выводит страницу оттдельного подраздела'''
    products = ElectroProduct.objects.filter(rubric=rubric_id)
    electro = Electro.objects.all()
    current_rubric = Electro.objects.get(pk=rubric_id)
    context = {
        'products':products,
        'electro':electro,
        'current_rubric':current_rubric
    }
    return render(request, 'products_list.html', context)

def get_rubric_santeh(request, rubric_id):
    '''Выводит страницу оттдельного подраздела'''
    products = SantehProduct.objects.filter(rubric=rubric_id)
    santeh = Santeh.objects.all()
    current_rubric = Santeh.objects.get(pk=rubric_id)
    context = {
        'products':products,
        'santeh':santeh,
        'current_rubric':current_rubric
    }
    return render(request, 'products_list.html', context)


def get_product_gas(request, rubric_id, gasproduct_id):
    product = GasProduct.objects.get(pk=gasproduct_id)
    context = {'product':product}
    return render(request, 'product.html', context)

def get_product_electro(request, rubric_id, electroproduct_id):
    product = ElectroProduct.objects.get(pk=electroproduct_id)
    context = {'product':product}
    return render(request, 'product.html', context)

def get_product_santeh(request, rubric_id, santehproduct_id):
    product = SantehProduct.objects.get(pk=santehproduct_id)
    context = {'product':product}
    return render(request, 'product.html', context)

def get_basket(request):
    return render(request, 'basket.html')