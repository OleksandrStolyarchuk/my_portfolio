from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.book = validated_data.get('book', instance.book)
        instance.user = validated_data.get('user', instance.user)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.end_at = validated_data.get('end_at', instance.end_at)
        instance.plated_end_at = validated_data.get('plated_end_at', instance.plated_end_at)
        instance.save()
        return instance
