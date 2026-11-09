from django.db import models
from django.db.models import Q


class OrderQuerySet(models.QuerySet):
    def available(self):
        return self.filter(status=self.model.Status.NEW)

    def active(self):
        return self.exclude(status__in=[
            self.model.Status.CANCELLED, self.model.Status.COMPLETED, self.model.Status.PAID,
        ])

    def search(self, term):
        return self.filter(Q(name__icontains=term) | Q(customer__name__icontains=term) |
                           Q(customer__second_name__icontains=term))

    def with_customer(self):
        return self.select_related('customer')
