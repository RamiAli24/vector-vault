from rest_framework import serializers


class BookSearchRequestSerializer(serializers.Serializer):
    """
    Serializer for book search request parameters.
    """

    title = serializers.CharField()


class BookSearchResponseSerializer(serializers.Serializer):
    """
    Serializer for returning book search results.
    """

    books = serializers.ListField(child=BookSearchRequestSerializer())
