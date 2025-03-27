from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from orders.forms import OrderForm
from orders.models import Order


def index(request):
    return HttpResponse("Test work.")


class CreateOrder(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/create_order.html'
    success_url = reverse_lazy('order_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.total_price = self.object.calculate_total()
        self.object.save()
        return response


class DeleteOrder(DeleteView):
    model = Order
    success_url = reverse_lazy('order_list')
    template_name = 'orders/confirm_delete.html'


class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'


class OrderUpdateView(UpdateView):
    model = Order
    fields = ['status']
    template_name = 'orders/order_update.html'
    success_url = reverse_lazy('order_list')
