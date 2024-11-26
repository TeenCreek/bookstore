from rest_framework import serializers

from .models import Author, Book


class BookTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для заголовка книги."""

    class Meta:
        model = Book
        fields = ('title',)
        extra_kwargs = {
            'title': {'help_text': 'Название книги'},
        }


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор для автора."""

    books = BookTitleSerializer(many=True, required=False)

    class Meta:
        model = Author
        fields = ('id', 'first_name', 'last_name', 'books')
        extra_kwargs = {
            'first_name': {'help_text': 'Имя автора'},
            'last_name': {'help_text': 'Фамилия автора'},
            'books': {'help_text': 'Список книг автора'},
        }

    def create(self, validated_data):
        """Создание автора с книгами."""

        books_data = validated_data.pop('books', [])

        author = Author.objects.create(**validated_data)

        if books_data:
            for book_data in books_data:
                Book.objects.create(author=author, **book_data)

        return author

    def update(self, instance, validated_data):
        """Обновление автора с книгами."""

        books_data = validated_data.pop('books', None)

        instance.first_name = validated_data.get(
            'first_name', instance.first_name
        )
        instance.last_name = validated_data.get(
            'last_name', instance.last_name
        )
        instance.save()

        if books_data is not None:
            for book_data in books_data:
                book_title = book_data.get('title')
                book, created = Book.objects.update_or_create(
                    title=book_title, author=instance, defaults=book_data
                )

        return instance


class AuthorNameSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения имени автора."""

    class Meta:
        model = Author
        fields = ('first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'help_text': 'Имя автора'},
            'last_name': {'help_text': 'Фамилия автора'},
        }


class BookSerializer(serializers.ModelSerializer):
    """Сериализатор для книги."""

    author = AuthorNameSerializer()

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'count')
        extra_kwargs = {
            'first_name': {'help_text': 'Имя автора'},
            'last_name': {'help_text': 'Фамилия автора'},
            'books': {'help_text': 'Список книг, написанных автором'},
        }

    def create(self, validated_data):
        """Создание книги с автором, если он есть в базе."""

        author_data = validated_data.pop('author')

        author, created = Author.objects.update_or_create(
            first_name=author_data['first_name'],
            last_name=author_data['last_name'],
        )

        book = Book.objects.create(author=author, **validated_data)

        return book

    def update(self, instance, validated_data):
        """Обновление книги с автором."""

        author_data = validated_data.pop('author')

        author, created = Author.objects.update_or_create(
            first_name=author_data['first_name'],
            last_name=author_data['last_name'],
        )

        instance.title = validated_data.get('title', instance.title)
        instance.author = author
        instance.count = validated_data.get('count', instance.count)
        instance.save()

        return instance
