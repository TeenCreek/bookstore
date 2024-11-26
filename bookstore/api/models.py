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

    title = models.CharField('Заголовок', max_length=FIELD_MAX_LENGTH)
    author = models.ForeignKey(
        Author,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='books',
    )
    count = models.IntegerField(
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

    def __str__(self):
        return f'Автор: {self.author} Заголовок: {self.title[:STR_MAX_LENGTH]}'

    def clean_count(self):
        if self.count < MIN_VALUE_AMOUNT:
            raise ValidationError(
                f'Остаток на складе не может быть меньше {MIN_VALUE_AMOUNT}'
            )
