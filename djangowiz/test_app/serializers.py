from rest_framework import serializers
from test_app.models import TimeStampMixin, BuyableType, Buyable, Property


class TimeStampMixinSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeStampMixin
        fields = '__all__'


class BuyableTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyableType
        fields = '__all__'


class BuyableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyable
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

