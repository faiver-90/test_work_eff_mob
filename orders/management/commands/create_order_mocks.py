import random
from django.core.management.base import BaseCommand
from orders.models import Order, Items, ChoiceStatus

class Command(BaseCommand):
    help = "Генерирует до 10 моковых заказов — не создаёт больше, если уже есть 10 или более"

    def handle(self, *args, **kwargs):
        items = list(Items.objects.all())
        if not items:
            self.stdout.write(self.style.ERROR("Нет блюд — сначала создайте записи в Items"))
            return

        existing = Order.objects.count()
        to_create = max(0, 10 - existing)

        if to_create == 0:
            self.stdout.write(self.style.WARNING("Уже есть 10 или более заказов — ничего не создаётся"))
            return

        for _ in range(to_create):
            table_number = random.randint(1, 20)
            order = Order.objects.create(table_number=table_number)
            chosen_items = random.sample(items, k=random.randint(1, min(5, len(items))))
            order.items.set(chosen_items)
            order.status = random.choice([status.value for status in ChoiceStatus])
            order.total_price = order.calculate_total()
            order.save()

        self.stdout.write(self.style.SUCCESS(f"Создано {to_create} новых заказов — всего теперь {Order.objects.count()}"))
