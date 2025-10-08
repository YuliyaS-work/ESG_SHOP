from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound

from .models import *

def get_basic(request):
    rubrics = Rubric.objects.prefetch_related('electro_set', 'gas_set', 'santeh_set').all()
    context = { 'rubrics': rubrics }
    return render(request, 'basic.html', context)

def get_main_page(request):
    ''' Отдает данные на главную страницу. '''
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
        # 'electro_subrubrics': electro_subrubrics,
        # 'gas_subrubrics': gas_subrubrics,
        # 'santeh_subrubrics': santeh_subrubrics
    }

    return render(request, 'catalog.html', context)

def get_rubric_gas(request, rubric_id):
    '''Выводит страницу оттдельного подраздела газового оборудования'''
    # current_rubric = get_object_or_404(Gas, pk=rubric_id)
    # products = GasProduct.objects.filter(rubric=current_rubric)
    # gas = Gas.objects.all()
    # context = {
    #     # 'products':products,
    #     # 'gas':gas,
    #     # 'current_rubric':current_rubric,
    #     'products': products,
    #     'current_rubric': current_rubric,
    #     'rubrics': Rubric.objects.prefetch_related('electro_set', 'gas_set', 'santeh_set').all(),  # для бокового меню
    #     'electro': Electro.objects.all(),
    #     'santeh': Santeh.objects.all(),
    #     'gas': Gas.objects.all(),
    # }
    # return render(request, 'products_list.html', context)
    products = GasProduct.objects.filter(rubric=rubric_id)
    gas = Gas.objects.all()
    current_rubric = Gas.objects.get(pk=rubric_id)
    context = {
        'products': products,
        'gas': gas,
        'current_rubric': current_rubric
    }
    return render(request, 'products_list.html', context)


def get_rubric_electro(request, rubric_id):
    '''Выводит страницу оттдельного подраздела'''
    # current_rubric = get_object_or_404(Electro, pk=rubric_id)
    # products = ElectroProduct.objects.filter(rubric=current_rubric)
    # electro = Electro.objects.all()
    # context = {
    #     # 'products':products,
    #     # 'electro':electro,
    #     # 'current_rubric':current_rubric,
    #     'products': products,
    #     'current_rubric': current_rubric,
    #     'rubrics': Rubric.objects.prefetch_related('electro_set', 'gas_set', 'santeh_set').all(),  # для бокового меню
    #     'electro': Electro.objects.all(),
    #     'santeh': Santeh.objects.all(),
    #     'gas': Gas.objects.all(),
    # }
    # return render(request, 'products_list.html', context)
    products = ElectroProduct.objects.filter(rubric=rubric_id)
    electro = Electro.objects.all()
    current_rubric = Electro.objects.get(pk=rubric_id)
    context = {
        'products': products,
        'electro': electro,
        'current_rubric': current_rubric
    }
    return render(request, 'products_list.html', context)

def get_rubric_santeh(request, rubric_id):
    '''Выводит страницу оттдельного подраздела'''
    # current_rubric = get_object_or_404(Santeh, pk=rubric_id)
    # products = SantehProduct.objects.filter(rubric=current_rubric)
    # santeh = Santeh.objects.all()
    # context = {
    #     # 'products':products,
    #     # 'santeh':santeh,
    #     # 'current_rubric':current_rubric,
    #     'products': products,
    #     'current_rubric': current_rubric,
    #     'rubrics': Rubric.objects.prefetch_related('electro_set', 'gas_set', 'santeh_set').all(),  # для бокового меню
    #     'electro': Electro.objects.all(),
    #     'santeh': Santeh.objects.all(),
    #     'gas': Gas.objects.all(),
    # }
    # return render(request, 'products_list.html', context)
    products = SantehProduct.objects.filter(rubric=rubric_id)
    santeh = Santeh.objects.all()
    current_rubric = Santeh.objects.get(pk=rubric_id)
    context = {
        'products': products,
        'santeh': santeh,
        'current_rubric': current_rubric
    }
    return render(request, 'products_list.html', context)

def get_product_gas(request, rubric_id, gasproduct_id):
    # product = get_object_or_404(GasProduct, pk=gasproduct_id)
    # current_rubric = product.rubric
    # context = {
    #     'product': product,
    #     'current_rubric': current_rubric,
    #     'rubrics': Rubric.objects.prefetch_related('electro_set', 'gas_set', 'santeh_set').all(),
    #     'electro': Electro.objects.all(),
    #     'santeh': Santeh.objects.all(),
    #     'gas': Gas.objects.all(),
    # }
    # return render(request, 'product.html', context)
    product = GasProduct.objects.get(pk=gasproduct_id)
    context = {'product': product}
    return render(request, 'product.html', context)

def get_product_electro(request, rubric_id, electroproduct_id):
    # product = get_object_or_404(ElectroProduct, pk=electroproduct_id)
    # current_rubric = product.rubric  # берем раздел товара
    # context = {
    #     'product': product,
    #     'current_rubric': current_rubric,
    #     'rubrics': Rubric.objects.prefetch_related('electro_set', 'gas_set', 'santeh_set').all(),
    #     'electro': Electro.objects.first(),
    #     'santeh': Santeh.objects.first(),
    #     'gas': Gas.objects.first(),
    # }
    # return render(request, 'product.html', context)
    product = ElectroProduct.objects.get(pk=electroproduct_id)
    context = {'product': product}
    return render(request, 'product.html', context)

def get_product_santeh(request, rubric_id, santehproduct_id):
    # product = get_object_or_404(SantehProduct, pk=santehproduct_id)
    # current_rubric = product.rubric
    # context = {
    #     'product': product,
    #     'current_rubric': current_rubric,
    #     'rubrics': Rubric.objects.prefetch_related('electro_set', 'gas_set', 'santeh_set').all(),
    #     'electro': Electro.objects.first(),
    #     'santeh': Santeh.objects.first(),
    #     'gas': Gas.objects.first(),
    # }
    # return render(request, 'product.html', context)
    product = SantehProduct.objects.get(pk=santehproduct_id)
    context = {'product': product}
    return render(request, 'product.html', context)
#
# def custom_404(request, exception):
#     return render(request, '404.html', status=404)