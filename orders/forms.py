from django import forms

from profiles.models import User
from .models import Order


class OrderFilterForm(forms.Form):
    q = forms.CharField(label='Название или заказчик', required=False, max_length=100)
    status = forms.ChoiceField(label='Статус', required=False, choices=[('', 'Все')] + Order.Status.choices)
    customer = forms.ModelChoiceField(label='Заказчик', required=False, queryset=User.objects.all())
    sort = forms.ChoiceField(label='Сортировка', required=False, choices=[
        ('id', 'По номеру'), ('name', 'По названию'), ('-id', 'Сначала новые'), ('customer', 'По заказчику')])
    page_size = forms.ChoiceField(label='Записей на странице', required=False, initial='5',
                                  choices=[('1', '1'), ('5', '5'), ('10', '10')])
