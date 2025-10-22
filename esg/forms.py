from django.forms import ModelForm

from esg.models import Order


class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = ("first_name", "last_name", "phone", "mail")
