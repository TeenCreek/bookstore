from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """Вьюсет для книги."""

    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author',)

    @action(methods=['post'], detail=True)
    def buy(self, request, pk):
        """Логика для покупки книги."""

        with transaction.atomic():
            book = get_object_or_404(Book, pk=pk)

            if book.count > 0:
                book.count = F('count') - 1
                book.save()
                book.refresh_from_db()

                return Response(
                    {'message': 'Книга успешно куплена'},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {'error': 'Книга не куплена, закончилась на складе'},
                status=status.HTTP_400_BAD_REQUEST,
            )


class AuthorViewSet(viewsets.ModelViewSet):
    """Вьюсет для автора."""

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
