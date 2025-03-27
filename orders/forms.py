from django import forms
from .models import Order, Items


class OrderForm(forms.ModelForm):
    """
    Форма для создания нового заказа.
    Поля:
      - table_number: номер стола (обязательное поле)
      - items: множественный выбор блюд (обязательно выбрать хотя бы одно)
    """
    items = forms.ModelMultipleChoiceField(
        queryset=Items.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Выберите блюда"
    )

    class Meta:
        model = Order
        fields = ['table_number', 'items']


class OrderEditForm(forms.ModelForm):
    """
    Форма для редактирования существующего заказа.
    Позволяет изменить:
      - table_number: номер стола
      - items: список выбранных блюд
      - status: текущий статус заказа
    """
    items = forms.ModelMultipleChoiceField(
        queryset=Items.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Блюда"
    )

    class Meta:
        model = Order
        fields = ['table_number', 'items', 'status']
