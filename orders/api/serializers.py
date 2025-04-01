from rest_framework import serializers
from orders.models import Order, Items


class ItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Items.
    Используется для чтения/записи полей id, name и price блюда.
    """

    class Meta:
        model = Items
        fields = ['id',
                  'name',
                  'price'
                  ]


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Order.
    При создании принимает список ID блюд, вычисляет total_price и сохраняет
    заказ.
    Поля total_price доступны только для чтения.
    """
    items = ItemSerializer(many=True, read_only=True)
    item_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Items.objects.all(),
        write_only=True
    )

    class Meta:
        model = Order
        fields = ['id',
                  'table_number',
                  'items',
                  'item_ids',
                  'total_price',
                  'status']
        read_only_fields = ['total_price', 'items']

    def create(self, validated_data):
        """
        Создаёт новый заказ: устанавливает блюда, рассчитывает total_price и
        сохраняет объект.
        """
        items = validated_data.pop('item_ids')
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
        if 'item_ids' in validated_data:
            items = validated_data.pop('item_ids')
            instance.items.set(items)
        return super().update(instance, validated_data)
