from celery import shared_task
from django.core.mail import send_mail

from ..models import Order, GasProduct, ElectroProduct, SantehProduct, GasOrder, ElectroOrder, SantehOrder
import esg_shop


@shared_task
def process_order_task(order_id, basket_cookies):
    order = Order.objects.get(pk=order_id)
    list_order = []

    for title, quantity in basket_cookies.items():
        if GasProduct.objects.filter(title=title).exists():
            product = GasProduct.objects.get(title=title)
            GasOrder.objects.create(order=order, gasproduct=product, quantity=quantity)
            list_order.append(f'{product.title} - {quantity}шт./м')
        elif ElectroProduct.objects.filter(title=title).exists():
            product = ElectroProduct.objects.get(title=title)
            ElectroOrder.objects.create(order=order, electroproduct=product, quantity=quantity)
            list_order.append(f'{product.title} - {quantity}шт./м')
        elif SantehProduct.objects.filter(title=title).exists():
            product = SantehProduct.objects.get(title=title)
            SantehOrder.objects.create(order=order, santehproduct=product, quantity=quantity)
            list_order.append(f'{product.title} - {quantity}шт./м')
    # for a seller
    subject = f'Новый заказ № {order.pk}'
    message = (f'Заказ № {order.pk} на имя {order.first_name} {order.last_name} ({order.phone}).\n' +
               f'Товары: \n' + '\n'.join(list_order))
    to_email = ['yuliyasorokinawork@gmail.com', 'tanyakuharskaya@gmail.com']

    # for a client
    subject1 = f'Магазин "Электротовары"'
    message1 = (f'{order.first_name}, номер Вашего заказа {order.pk}.')
    to_email1 = [f'{order.mail}']

    try:
        # email to a seller
        send_mail(
            subject=subject,
            message=message,
            from_email=esg_shop.settings.DEFAULT_FROM_EMAIL,
            recipient_list=to_email,
            fail_silently=False,
        )
        # email to a client
        send_mail(
            subject=subject1,
            message=message1,
            from_email=esg_shop.settings.DEFAULT_FROM_EMAIL,
            recipient_list=to_email1,
            fail_silently=False,
        )
    except Exception as e:
        print(f'❌ Письмо не отправлено: {e}')


# @shared_task
# def send_order_email_task(to_email, subject, message):
#     print(f'📤 Отправка письма: {subject} → {to_email}')
#     print(f'📦 Содержимое:\n{message}')
#     try:
#         send_mail(
#             subject=subject,
#             message=message,
#             from_email=esg_shop.settings.DEFAULT_FROM_EMAIL,
#             recipient_list=to_email,
#             fail_silently=False,
#         )
#     except Exception as e:
#         print(f'❌ Письмо не отправлено: {e}')