from django.db import models
from django.urls import reverse


class User(models.Model):
    name = models.CharField('Имя', max_length=100)
    second_name = models.CharField('Фамилия', max_length=100, blank=True)
    role = models.CharField('Роль', max_length=30)
    email = models.CharField('Контакт', max_length=254, blank=True)
    password = models.CharField('Хеш пароля', max_length=128, editable=False, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self):
        return f'{self.name} {self.second_name}'.strip()

    def get_absolute_url(self):
        return reverse('profiles:detail', args=[self.pk])
