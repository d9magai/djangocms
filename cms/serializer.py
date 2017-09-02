# coding: utf-8

from rest_framework import serializers

from cms.models import Book, Impression


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'name', 'publisher', 'page')


class ImpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Impression
        fields = ('id', 'comment', 'book_id')
