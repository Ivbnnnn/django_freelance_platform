from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Review(models.Model):
    order = models.ForeignKey(
        'orders.Order', verbose_name='Заказ', related_name='reviews',
        on_delete=models.PROTECT, null=True, blank=True,
    )
    source_order_id = models.CharField('Исходный ID', max_length=100, blank=True, editable=False)
    author = models.ForeignKey(
        'profiles.User', verbose_name='Автор', related_name='reviews',
        on_delete=models.PROTECT, null=True, blank=True,
    )
    source_author_id = models.CharField('Исходный ID', max_length=100, blank=True, editable=False)
    rating = models.PositiveSmallIntegerField('Оценка', validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField('Текст', blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [models.CheckConstraint(condition=models.Q(rating__gte=1, rating__lte=5), name='review_rating_1_5')]

    def __str__(self):
        return f'Отзыв №{self.pk}'
