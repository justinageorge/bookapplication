from rest_framework import serializers
from book.models import Books


class BookSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model=Books
        fields="__all__"