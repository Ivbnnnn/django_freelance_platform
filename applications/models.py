from django.db import models


class Application(models.Model):
    order = models.ForeignKey('orders.Order', verbose_name='Заказ', related_name='applications',
                                    on_delete=models.PROTECT, null=True, blank=True)
    source_order_id = models.CharField('Исходный ID', max_length=100, blank=True, editable=False)
    executor = models.ForeignKey('profiles.User', verbose_name='Исполнитель', related_name='applications',
                                    on_delete=models.PROTECT, null=True, blank=True)
    source_executor_id = models.CharField('Исходный ID', max_length=100, blank=True, editable=False)
    comment = models.TextField('Комментарий', blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'

    def __str__(self):
        return f'Отклик №{self.pk}'
