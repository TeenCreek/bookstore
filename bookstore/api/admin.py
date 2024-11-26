from django.contrib import admin

from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Админка для автора."""

    list_display = ('id', 'first_name', 'last_name', 'book_count')
    search_fields = ('first_name', 'last_name')
    ordering = ('id',)

    def book_count(self, obj):
        """Количество книг у автора."""

        return obj.books.count()

    book_count.short_description = 'Количество книг'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Админка для управления книгами."""

    list_display = ('id', 'title', 'author', 'count')
    list_filter = ('author',)
    search_fields = ('title',)
    ordering = ('id',)
    list_editable = ('count',)
