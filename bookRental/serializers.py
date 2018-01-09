from . import models
from rest_framework import serializers
from django.contrib.auth import get_user_model
UserModel = get_user_model()


class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Author
        fields = ['first_name', 'last_name', 'url', 'id']


class BookSerializer(serializers.HyperlinkedModelSerializer):

    author = serializers.SlugRelatedField(many=False, read_only=True, slug_field='full_name')

    class Meta:
        model = models.Book
        fields = ['url', 'id', 'name', 'author', 'price']


class BookRentalSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Book
        fields = ['url', 'name']


class RentalSerializer(serializers.HyperlinkedModelSerializer):
    book = BookRentalSerializer(many=False)

    class Meta:
        model = models.Lease
        fields = ['book', 'balance']
