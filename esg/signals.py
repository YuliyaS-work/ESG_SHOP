from django.dispatch import receiver, Signal

from .models import *

get_cookies = Signal()

@receiver(get_cookies, sender=Order, dispatch_uid='unique_identifier')
def add_cookies(sender, instance, basket_cookies, **kwargs):
    for title, quantity in basket_cookies.items():
        if GasProduct.objects.filter(title=title).exists():
            product = GasProduct.objects.get(title=title)
            gasorder = GasOrder(order_id=instance.pk, gasproduct_id=product.pk, quantity=quantity)
            gasorder.save()
        elif ElectroProduct.objects.filter(title=title).exists():
            product = ElectroProduct.objects.get(title=title)
            electroorder = ElectroOrder(order_id=instance.pk, electroproduct_id=product.pk, quantity=quantity)
            electroorder.save()
        elif SantehProduct.objects.filter(title=title).exists():
            product = SantehProduct.objects.get(title=title)
            santehorder = SantehOrder(order_id=instance.pk, santehproduct_id=product.pk, quantity=quantity)
            santehorder.save()






