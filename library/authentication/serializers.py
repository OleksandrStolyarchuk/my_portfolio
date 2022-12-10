from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import CustomUser
from order.serializers import OrderSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    orders = OrderSerializer(many=True, required=False)

    class Meta:
        model = CustomUser
        fields = ('url', 'id', 'email', 'password', 'first_name', 'last_name', 'role', 'orders')

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.role = validated_data.get('role', instance.role)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
