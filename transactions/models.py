from django.core.validators import MinValueValidator
from django.db import models


class Transaction(models.Model):
    order = models.ForeignKey('orders.Order', verbose_name='Заказ', related_name='transactions',
                                    on_delete=models.PROTECT, null=True, blank=True)
    source_order_id = models.CharField('Исходный ID', max_length=100, blank=True, editable=False)
    amount = models.DecimalField('Сумма', max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField('Статус', max_length=20, choices=[('pending', 'Ожидает оплаты'), ('paid', 'Оплачен'), ('cancelled', 'Отменён')], default='pending', db_index=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
        constraints = [models.CheckConstraint(condition=models.Q(amount__gte=0), name='transaction_nonnegative')]

    def __str__(self):
        return f'Платёж №{self.pk}'
