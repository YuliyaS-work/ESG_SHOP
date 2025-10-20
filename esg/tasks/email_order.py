from celery import shared_task
from django.core.mail import send_mail

import esg_shop


@shared_task
def send_order_email_task(to_email, subject, message):
    print(f'📤 Отправка письма: {subject} → {to_email}')
    print(f'📦 Содержимое:\n{message}')
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=esg_shop.settings.DEFAULT_FROM_EMAIL,
            recipient_list=to_email,
            fail_silently=False,
        )
    except Exception as e:
        print(f'❌ Письмо не отправлено: {e}')