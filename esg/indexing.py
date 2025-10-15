from esg.documents import (
    ElectroProductDocument,
    GasProductDocument,
    SantehProductDocument
)
from esg.models import ElectroProduct, GasProduct, SantehProduct


def index_all_products():
    # Инициализация индексов
    ElectroProductDocument.init()
    GasProductDocument.init()
    SantehProductDocument.init()

    # Индексация данных
    for product in ElectroProduct.objects.all():
        ElectroProductDocument().update(product)

    for product in GasProduct.objects.all():
        GasProductDocument().update(product)

    for product in SantehProduct.objects.all():
        SantehProductDocument().update(product)