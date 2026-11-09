"""Explicit, atomic import from the read-only PR7 database into Django's database."""
import sqlite3
from contextlib import closing
from pathlib import Path

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from profiles.models import User
from orders.models import Order
from applications.models import Application
from transactions.models import Transaction
from reviews.models import Review


class Command(BaseCommand):
    help = 'Перенос данных ПР7 в пустые таблицы ORM без изменения исходной базы'

    def add_arguments(self, parser):
        parser.add_argument('--source', type=Path, default=settings.BASE_DIR / 'data/freelance.sqlite')

    @transaction.atomic
    def handle(self, *args, **options):
        models = [('users', User), ('orders', Order), ('applications', Application),
                  ('transactions', Transaction), ('reviews', Review)]
        if any(model.objects.exists() for _, model in models):
            raise CommandError('Таблицы ORM не пусты. Повторный импорт остановлен без изменения данных.')
        path = options['source'].resolve()
        if not path.is_file():
            raise CommandError(f'Исходная база не найдена: {path}')
        try:
            with closing(sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)) as conn:
                conn.row_factory = sqlite3.Row
                for table, model in models:
                    rows = conn.execute(f'SELECT * FROM {table} ORDER BY id').fetchall()
                    for row in rows:
                        values = dict(row)
                        if table == 'users':
                            values['password'] = make_password(values['password'])
                        model.objects.create(**values)
                    self.stdout.write(f'{table}: {len(rows)}')
        except (sqlite3.Error, ValueError) as exc:
            raise CommandError(f'Импорт отменён: {exc}') from exc
        self.stdout.write(self.style.SUCCESS('Данные перенесены. Исходная база не изменена.'))
