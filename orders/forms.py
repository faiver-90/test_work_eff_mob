from django import forms
from .models import Order, Items


class OrderForm(forms.ModelForm):
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
    items = forms.ModelMultipleChoiceField(
        queryset=Items.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Блюда"
    )

    class Meta:
        model = Order
        fields = ['table_number', 'items', 'status']
