from django.db import models


class Items(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)


class ChoiceStatus(models.IntegerChoices):
    WAITING = 1, "в ожидании"
    DONE = 2, "готово"
    PAID = 3, "оплачено"


class Order(models.Model):
    table_number = models.IntegerField()
    items = models.ManyToManyField(Items, related_name="orders")
    total_price = models.DecimalField(max_digits=10,
                                      decimal_places=2,
                                      null=True,
                                      blank=True)
    status = models.IntegerField(choices=ChoiceStatus.choices,
                                 default=ChoiceStatus.WAITING)

    def calculate_total(self):
        return sum(item.price for item in self.items.all())

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total()
        super().save(*args, **kwargs)
