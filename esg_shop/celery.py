import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'esg_shop.settings')

app = Celery('esg_shop', broker='redis://localhost:6379/0')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(
    CELERY_IMPORTS=('esg.tasks.email_order',),
)

app.autodiscover_tasks(['esg'])