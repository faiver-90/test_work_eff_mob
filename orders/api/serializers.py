from rest_framework import serializers
from orders.models import Order, Items


class ItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Items.
    Используется для чтения/записи полей id, name и price блюда.
    """

    class Meta:
        model = Items
        fields = ['id', 'name', 'price']


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Order.
    При создании принимает список ID блюд, вычисляет total_price и сохраняет
    заказ.
    Поля total_price доступны только для чтения.
    """
    items = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Items.objects.all()
    )

    class Meta:
        model = Order
        fields = ['id', 'table_number', 'items', 'total_price', 'status']
        read_only_fields = ['total_price']

    def create(self, validated_data):
        """
        Создаёт новый заказ: устанавливает блюда, рассчитывает total_price и
        сохраняет объект.
        """
        items = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        order.items.set(items)
        order.total_price = order.calculate_total()
        order.save()
        return order

    def update(self, instance, validated_data):
        """
        При обновлении заказа обновляет список блюд, если передан параметр
        items, затем вызывает стандартное поведение ModelSerializer.update().
        """
        if 'items' in validated_data:
            instance.items.set(validated_data.pop('items'))
        return super().update(instance, validated_data)
