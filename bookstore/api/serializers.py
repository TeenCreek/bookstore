from rest_framework import serializers

from .models import Author, Book


class BookTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для заголовка книги."""

    class Meta:
        model = Book
        fields = ('title',)


class AuthorNameSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения имени автора."""

    class Meta:
        model = Author
        fields = ('first_name', 'last_name')


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор для автора."""

    books = BookTitleSerializer(many=True)

    class Meta:
        model = Author
        fields = ('id', 'first_name', 'last_name', 'books')

    def create(self, validated_data):
        """Создание автора с книгами."""

        books_data = validated_data.pop('books', [])
        author = Author.objects.create(**validated_data)

        if books_data:
            for book_data in books_data:
                Book.objects.create(author=author, **book_data)

        return author

    def update(self, instance, validated_data):
        """Обновление автора и его книг."""

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


class BookSerializer(serializers.ModelSerializer):
    """Сериализатор для книги."""

    author = AuthorNameSerializer()

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'count')

    def create(self, validated_data):
        """Создание книги с автором."""

        author_data = validated_data.pop('author')

        author, created = Author.objects.get_or_create(
            first_name=author_data['first_name'],
            last_name=author_data['last_name'],
        )

        if Book.objects.filter(
            title=validated_data['title'], author=author
        ).exists():
            raise serializers.ValidationError(
                'Книга с таким названием уже существует у этого автора.'
            )

        return Book.objects.create(author=author, **validated_data)

    def update(self, instance, validated_data):
        """Обновление книги с автором."""

        author_data = validated_data.pop('author', None)
        if author_data:
            author, created = Author.objects.get_or_create(
                first_name=author_data['first_name'],
                last_name=author_data['last_name'],
            )
            instance.author = author

        instance.title = validated_data.get('title', instance.title)
        instance.count = validated_data.get('count', instance.count)

        if (
            Book.objects.filter(title=instance.title, author=instance.author)
            .exclude(id=instance.id)
            .exists()
        ):
            raise serializers.ValidationError(
                'Книга с таким названием уже существует у этого автора.'
            )

        instance.save()
        return instance

    def validate(self, attrs):
        """Проверка уникальности книги у конкретного автора."""

        author_data = attrs.get('author')

        if Book.objects.filter(
            title=attrs.get('title'),
            author__first_name=author_data['first_name'],
            author__last_name=author_data['last_name'],
        ).exists():
            raise serializers.ValidationError(
                'Книга с таким названием уже существует у этого автора.'
            )

        return attrs
