from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

STR_MAX_LENGTH = 25
MIN_VALUE_AMOUNT = 0
DEFAULT_VALUE_AMOUNT = 100
FIELD_MAX_LENGTH = 100


class Author(models.Model):
    """Модель для автора."""

    first_name = models.CharField('Имя', max_length=FIELD_MAX_LENGTH)
    last_name = models.CharField('Фамилия', max_length=FIELD_MAX_LENGTH)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    """Модель для книги."""

    title = models.CharField(
        'Заголовок', max_length=FIELD_MAX_LENGTH, db_index=True
    )
    author = models.ForeignKey(
        Author,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='books',
        db_index=True,
    )
    count = models.PositiveIntegerField(
        'Остаток на складе',
        default=DEFAULT_VALUE_AMOUNT,
        validators=[
            MinValueValidator(
                MIN_VALUE_AMOUNT,
                message=f'Минимальное значение {MIN_VALUE_AMOUNT}',
            )
        ],
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        indexes = (
            models.Index(fields=['title']),
            models.Index(fields=['author']),
        )
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'), name='unique_for_author_book'
            ),
        )

    def __str__(self):
        return f'Автор: {self.author} Заголовок: {self.title[:STR_MAX_LENGTH]}'
