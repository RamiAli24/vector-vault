import logging

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from vector_vault.api.models import Book
from vector_vault.api.serializers import BookSearchRequestSerializer, BookSearchResponseSerializer

logger = logging.getLogger(__name__)


class BookView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="title",
                type=str,
                location=OpenApiParameter.QUERY,
                required=True,
                description="Title to match",
                style="form",
                explode=True,
            )
        ],
        responses={200: BookSearchResponseSerializer},
    )
    def get(self, request):
        """
        Endpoint to query Books.
        """
        title = request.query_params.get("title")
        if not title:
            return Response({"error": "Title parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        books = Book.search(title)

        response_serializer = BookSearchResponseSerializer({"books": books})
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=BookSearchRequestSerializer,
        responses={200: BookSearchRequestSerializer},
    )
    def post(self, request):
        """
        Endpoint to add a new Book.
        """
        request_serializer = BookSearchRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        user = None
        if request.user.is_authenticated:
            user = request.user

        obj = Book.objects.create(**request_serializer.validated_data, created_by=user)
        print("obj.title", obj.title)
        response = {"uuid": obj.uuid, "title": obj.title}
        response_serializer = BookSearchRequestSerializer(response)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
