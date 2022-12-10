from rest_framework import serializers
from author.models import Author
from .models import Book

# class BookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         fields = ('__all__')
#
#     def create(self, validated_data):
#         return Book.objects.create(**validated_data)

class BookSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
    description = serializers.CharField(max_length=256)
    count = serializers.IntegerField()
    id = serializers.IntegerField()
    publication_year = serializers.IntegerField()
    date_of_issue = serializers.DateField(read_only=True)

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.count = validated_data.get('count', instance.count)
        instance.id = validated_data.get('id', instance.id)
        instance.publication_year = validated_data.get('publication_year', instance.publication_year)
        instance.date_of_issue = validated_data.get('date_of_issue', instance.date_of_issue)
        instance.save()
        return instance