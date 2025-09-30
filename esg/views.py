from django.shortcuts import render

from .models import *


def get_main_page(request):
    pass
    return render(request, 'main_page.html')


def get_catalog(request):
    rubrics = Rubric.objects.prefetch_related('electro_set', 'gas_set', 'santeh_set').all()
    electro_subrubrics = Electro.objects.prefetch_related('electroproduct_set').all()
    gas_subrubrics = Gas.objects.prefetch_related('gasproduct_set').all()
    santeh_subrubrics = Electro.objects.prefetch_related('santehproduct_set').all()

    context = {
        'rubrics': rubrics,
        'electro_subrubrics': electro_subrubrics,
        'gas_subrubrics': gas_subrubrics,
        'santeh_subrubrics': santeh_subrubrics
    }

    return render(request, 'catalog.html', context)

