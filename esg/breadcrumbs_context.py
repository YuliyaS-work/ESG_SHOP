from django.urls import resolve, reverse
from .models import Rubric, Gas, Electro, Santeh, GasProduct, ElectroProduct, SantehProduct

# Универсальная карта моделей
RUBRIC_MODELS = {
    'Газификация': {
        'subrubric': Gas,
        'product': GasProduct,
    },
    'Электрика': {
        'subrubric': Electro,
        'product': ElectroProduct,
    },
    'Сантехника': {
        'subrubric': Santeh,
        'product': SantehProduct,
    },
}

def breadcrumbs_context(request):
    crumbs = [{'label': 'Главная', 'url': reverse('main')}]

    try:
        match = resolve(request.path_info)
        kwargs = match.kwargs
        view_name = match.view_name

        # Каталог
        if view_name.startswith('catalog') or 'rubric_id' in kwargs:
            crumbs.append({'label': 'Каталог', 'url': reverse('catalog')})

        # Раздел
        rubric_id = kwargs.get('rubric_id')
        rubric = Rubric.objects.filter(pk=rubric_id).first() if rubric_id else None

        if rubric:
            crumbs.append({
                'label': rubric.rubric_name,
                'url': reverse('subrubrics', kwargs={'rubric_id': rubric_id})
            })

            model_map = RUBRIC_MODELS.get(rubric.rubric_name)

            # Подраздел
            subrubric_id = kwargs.get('subrubric_id')
            if subrubric_id and model_map:
                SubrubricModel = model_map['subrubric']
                subrubric = SubrubricModel.objects.filter(pk=subrubric_id).first()
                if subrubric:
                    crumbs.append({
                        'label': getattr(subrubric, 'name', str(subrubric)),
                        'url': reverse('products', kwargs={'rubric_id': rubric_id, 'subrubric_id': subrubric_id})
                    })

            # Товар
            product_id = kwargs.get('product_id')
            if product_id and model_map:
                ProductModel = model_map['product']
                product = ProductModel.objects.filter(pk=product_id).first()
                if product:
                    crumbs.append({
                        'label': getattr(product, 'name', str(product.title)),
                        'url': reverse('product', kwargs={'rubric_id': rubric_id, 'subrubric_id': subrubric_id, 'product_id': product_id})
                    })

    except Exception as e:
        print(f'Breadcrumb error: {e}')

    return {'breadcrumbs': crumbs}