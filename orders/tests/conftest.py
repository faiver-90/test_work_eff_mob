import pytest

from orders.models import Items, Order


@pytest.fixture
def test_create_item():
    return Items.objects.create(name="Борщ", price=300)


@pytest.fixture
def test_create_order():
    return Order.objects.create(table_number=1)
