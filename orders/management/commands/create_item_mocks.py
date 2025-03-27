import random
from django.core.management.base import BaseCommand

from orders.models import Items


class Command(BaseCommand):
    help = "Генерирует моковые данные: создаёт 10 уникальных блюд," \
           " не создавая дубликаты"

    def handle(self, *args, **kwargs):
        dishes = [
            "Борщ", "Салат Цезарь", "Пельмени", "Бефстроганов",
            "Оливье", "Суши", "Паста Карбонара", "Пицца Маргарита",
            "Куриный суп", "Тирамису"
        ]

        created_count = 0

        for name in dishes:
            price = random.randint(100, 1000)
            item, created = Items.objects.get_or_create(
                name=name,
                defaults={'price': price}
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Успешно создано {created_count} новых блюд"
        ))
