from rest_framework import serializers

from .forms import OrderForm
from .models import Order, Feedback, Electro, Gas, Santeh


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ("first_name", "last_name", "phone", "mail")


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ("name", "phone", "subject", "message")