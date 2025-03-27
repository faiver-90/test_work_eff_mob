from rest_framework import serializers
from orders.models import Order, Items


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ['id', 'name', 'price']


class OrderSerializer(serializers.ModelSerializer):
    # Принимаем список ID при записи…
    items = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Items.objects.all()
    )

    class Meta:
        model = Order
        fields = ['id', 'table_number', 'items', 'total_price', 'status']
        read_only_fields = ['total_price']

    def create(self, validated_data):
        items = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        order.items.set(items)
        order.total_price = order.calculate_total()
        order.save()
        return order

    def update(self, instance, validated_data):
        if 'items' in validated_data:
            instance.items.set(validated_data.pop('items'))
        return super().update(instance, validated_data)