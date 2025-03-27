from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, \
    TemplateView

from orders.forms import OrderForm
from orders.models import Order, ChoiceStatus


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

    def get_queryset(self):
        qs = super().get_queryset()
        table = self.request.GET.get('table_number')
        status = self.request.GET.get('status')
        if table:
            qs = qs.filter(table_number=table)
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['statuses'] = Order.STATUS_CHOICES
        ctx['selected_table'] = self.request.GET.get('table_number', '')
        ctx['selected_status'] = self.request.GET.get('status', '')
        return ctx


class OrderUpdateView(UpdateView):
    model = Order
    fields = ['status']
    template_name = 'orders/order_update.html'
    success_url = reverse_lazy('order_list')


class RevenueView(TemplateView):
    template_name = 'orders/revenue.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        paid_qs = Order.objects.filter(status=ChoiceStatus.PAID)
        ctx['total_revenue'] = paid_qs.aggregate(total=Sum('total_price'))[
                                   'total'] or 0
        ctx['paid_orders'] = paid_qs
        return ctx
