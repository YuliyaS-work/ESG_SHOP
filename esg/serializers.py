from rest_framework import serializers

from .forms import OrderForm
from .models import Order, Feedback, Electro, Gas, Santeh


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ("first_name", "last_name", "phone")


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ("name", "phone", "subject", "message")

# =нужны бфли для js для вывода списка подрубрик
# class ElectroSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Electro
#         fields = ("title", "id", "rubric")
#
#
# class GasSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Gas
#         fields = ("title", "id", "rubric")
#
#
# class SantehSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Santeh
#         fields = ("title", "id", "rubric")

