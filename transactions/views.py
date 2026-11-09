from django.shortcuts import get_object_or_404, render

from .models import Transaction


def index(request):
    records = Transaction.objects.all().select_related('order')
    return render(request, 'transactions/transaction_list.html', {'transactions': records})


def detail(request, transaction_id):
    record = get_object_or_404(Transaction.objects.select_related('order'), pk=transaction_id)
    return render(request, 'transactions/transaction_detail.html', {'transaction': record})
