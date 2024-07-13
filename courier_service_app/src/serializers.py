from rest_framework import serializers
from . import models

class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Courier
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = '__all__'

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Branch
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'

class ProductSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductSet
        fields = '__all__'
