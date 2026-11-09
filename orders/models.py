from django.db import models
from django.urls import reverse


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'Новый'
        IN_PROGRESS = 'in_progress', 'В работе'
        PAID = 'paid', 'Оплачен'
        COMPLETED = 'completed', 'Завершён'
        CANCELLED = 'cancelled', 'Отменён'

    name = models.CharField('Название', max_length=255)
    budget = models.CharField('Бюджет или диапазон', max_length=100)
    customer = models.ForeignKey('profiles.User', verbose_name='Заказчик', related_name='orders',
                                 on_delete=models.PROTECT, null=True, blank=True)
    source_customer_id = models.CharField('Исходный ID заказчика', max_length=100, blank=True, editable=False)
    status = models.CharField('Статус', max_length=20, choices=Status.choices, default=Status.NEW, db_index=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('orders:detail', args=[self.pk])
