from rest_framework import serializers

from esg.forms import OrderForm
from esg.models import Order, Feedback


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ("first_name", "last_name", "phone")


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ("name", "phone", "subject", "message")
