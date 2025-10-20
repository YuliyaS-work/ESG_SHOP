from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

from .models import *
from .tasks.email_order import send_order_email_task

get_cookies = Signal()


@receiver(get_cookies, sender=Order, dispatch_uid='unique_identifier')
def add_cookies(sender, instance, basket_cookies, **kwargs):
    list_order = []
    for title, quantity in basket_cookies.items():
        if GasProduct.objects.filter(title=title).exists():
            product = GasProduct.objects.get(title=title)
            gasorder = GasOrder(order_id=instance.pk, gasproduct_id=product.pk, quantity=quantity)
            gasorder.save()
            list_order.append(f'{product.title} - {quantity}шт./м')
        elif ElectroProduct.objects.filter(title=title).exists():
            product = ElectroProduct.objects.get(title=title)
            electroorder = ElectroOrder(order_id=instance.pk, electroproduct_id=product.pk, quantity=quantity)
            electroorder.save()
            list_order.append(f'{product.title} - {quantity}шт./м')
        elif SantehProduct.objects.filter(title=title).exists():
            product = SantehProduct.objects.get(title=title)
            santehorder = SantehOrder(order_id=instance.pk, santehproduct_id=product.pk, quantity=quantity)
            santehorder.save()
            list_order.append(f'{product.title} - {quantity}шт./м')

    subject = f'Новый заказ № {instance.pk}'
    message = (f'Заказ № {instance.pk} на имя {instance.first_name} {instance.last_name} ({instance.phone}).\n'+
               f'Товары: \n' + '\n'.join(list_order))
    to_email = ['yuliyasorokinawork@gmail.com', 'tanyakuharskaya@gmail.com']
    print(f'📨 Запуск задачи: {to_email}, {subject}, {message}')
    send_order_email_task.delay(to_email=to_email, subject=subject, message=message)

# @receiver(get_cookies, sender=Order, dispatch_uid='unique_identifier')
# def add_cookies(sender, instance, basket_cookies, **kwargs):
#     for title, quantity in basket_cookies.items():
#         if GasProduct.objects.filter(title=title).exists():
#             product = GasProduct.objects.get(title=title)
#             gasorder = GasOrder(order_id=instance.pk, gasproduct_id=product.pk, quantity=quantity)
#             gasorder.save()
#         elif ElectroProduct.objects.filter(title=title).exists():
#             product = ElectroProduct.objects.get(title=title)
#             electroorder = ElectroOrder(order_id=instance.pk, electroproduct_id=product.pk, quantity=quantity)
#             electroorder.save()
#         elif SantehProduct.objects.filter(title=title).exists():
#             product = SantehProduct.objects.get(title=title)
#             santehorder = SantehOrder(order_id=instance.pk, santehproduct_id=product.pk, quantity=quantity)
#             santehorder.save()
#
# @receiver(post_save, sender=Order)
# def order_mail_handler(sender, instance, created, **kwargs):
#     if created:
#         list_order = [3]
#         subject = f'Новый заказ № {instance.pk}'
#         message = f'Заказ № {instance.pk} на имя {instance.first_name} {instance.last_name} ({instance.phone}).\
#         \ Товары: {list_order}'
#         to_email = ['yuliyasorokinawork@gmail.com', 'tanyakuharskaya@gmail.com']
#         send_order_email_task.delay(to_email, subject, message)

