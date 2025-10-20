from celery import shared_task
from django.core.mail import send_mail

from ..models import Feedback
import esg_shop


@shared_task
def process_feedback_task(feedback_id):
    feedback = Feedback.objects.get(pk=feedback_id)
    subject = f'Обратная связь № {feedback.pk}'
    message = (f'Обратная связь № {feedback.pk} для {feedback.name} ({feedback.phone}).\n' +
               f'Тема: \n' + f'{feedback.subject} \n' +
               f'Сообщение: \n' + f'{feedback.message}'
    )
    to_email = ['yuliyasorokinawork@gmail.com', 'tanyakuharskaya@gmail.com']
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