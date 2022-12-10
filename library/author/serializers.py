from rest_framework import serializers

from author.models import Author

from book.models import Book


class AuthorSerializer(serializers.ModelSerializer):
    # books = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), many=True)
    class Meta:
        books = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), many=True)
        model = Author
        fields = '__all__'
        # fields = ('id', 'name', 'surname', 'patronymic' )

    def create(self, validated_data):
        author = Author.objects.create(
            name=validated_data['name'],
            surname=validated_data['surname'],
            patronymic=validated_data['patronymic'],
            id=validated_data['id'],
            # books = request.data['books']
        )
        for book_id in validated_data['books']:
            author.books.add(book_id)
        return author
        # return Author.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.patronymic = validated_data.get('patronymic', instance.patronymic)
        instance.books = validated_data.get('books', instance.books)
        instance.id = validated_data.get('id', instance.id)
        instance.save()
        return instance