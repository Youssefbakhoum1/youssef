# LittleLemonAPI/serializers.py

from rest_framework import serializers
from .models import MenuItem
from decimal import Decimal
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category']
    
    def calculate_tax(self, product: MenuItem):
        return product.price * Decimal(1.1)
# LittleLemonAPI/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User

class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',)  # Add any fields needed for deletion

    def delete(self, instance):
        instance.delete()
        return instance


