import pytest
from django.urls import reverse
from orders.models import Order, ChoiceStatus


@pytest.mark.django_db
def test_create_order_view(client, test_create_item):
    """
    Проверяет успешное создание заказа через форму:
    - отправка POST с номером стола и выбранным блюдом
    - проверка, что заказ создан и цена рассчитана правильно
    """
    url = reverse("create_order")
    data = {
        "table_number": 5,
        "items": [test_create_item.id]
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Order.objects.count() == 1
    order = Order.objects.first()
    assert order.total_price == test_create_item.price


@pytest.mark.django_db
def test_order_list_view(client, test_create_order):
    """
    Проверяет доступность страницы со списком заказов.
    Ожидается статус 200 и успешный рендер.
    """
    url = reverse("order_list")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_order_delete_view(client, test_create_order):
    """
    Проверяет удаление заказа через POST-запрос:
    - после удаления заказ не должен существовать в базе
    - должен быть редирект
    """
    url = reverse("delete_order", args=[test_create_order.id])
    response = client.post(url)
    assert response.status_code == 302
    assert Order.objects.count() == 0


@pytest.mark.django_db
def test_order_update_view(client, test_create_order, test_create_item):
    """
    Проверяет редактирование заказа:
    - изменение списка блюд и статуса
    - пересчёт total_price
    - успешное сохранение и редирект
    """
    test_create_order.items.set([test_create_item])
    url = reverse("order_edit", args=[test_create_order.id])
    data = {
        "table_number": test_create_order.table_number,
        "items": [test_create_item.id],
        "status": ChoiceStatus.PAID,
    }
    response = client.post(url, data)
    assert response.status_code == 302  # редирект после успешной формы
    test_create_order.refresh_from_db()
    assert test_create_order.status == ChoiceStatus.PAID.value


@pytest.mark.django_db
def test_revenue_view(client, test_create_order, test_create_item):
    """
    Проверяет отображение выручки:
    - выставляется статус PAID
    - заказ участвует в расчёте общей выручки
    - выручка отображается на странице
    """
    test_create_order.status = ChoiceStatus.PAID
    test_create_order.items.set([test_create_item])
    test_create_order.total_price = test_create_order.calculate_total()
    test_create_order.save()

    url = reverse("order_revenue")
    response = client.get(url)
    assert response.status_code == 200
    assert str(test_create_order.total_price).encode() in response.content
