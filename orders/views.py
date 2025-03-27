from django.db.models import Sum
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, \
    UpdateView, TemplateView

from orders.forms import OrderForm, OrderEditForm
from orders.models import Order, ChoiceStatus


def index(request):
    """
    Простая функция-представление для проверки работоспособности приложения.
    Возвращает HTTPResponse с текстом 'Test work.'.
    """
    return HttpResponse("Test work.")


class CreateOrder(CreateView):
    """
   Представление для создания нового заказа.
   Автоматически рендерит форму OrderForm и сохраняет объект Order.
   После успешного создания рассчитывает и сохраняет total_price заказа.
   """
    model = Order
    form_class = OrderForm
    template_name = 'orders/create_order.html'
    success_url = reverse_lazy('order_list')

    def form_valid(self, form):
        """
        Вызывается после валидации формы.
        Сохраняет новый заказ, рассчитывает total_price и обновляет объект.
        """
        try:
            response = super().form_valid(form)
            self.object.total_price = self.object.calculate_total()
            self.object.save()
            return response
        except Exception as e:
            form.add_error(None, "Ошибка при сохранении заказа")
            return self.form_invalid(form)


class DeleteOrder(DeleteView):
    """
      Представление для удаления заказа.
      Отображает страницу подтверждения удаления и удаляет объект по POST.
      """
    model = Order
    success_url = reverse_lazy('order_list')
    template_name = 'orders/confirm_delete.html'


class OrderListView(ListView):
    """
    Представление для отображения списка заказов с фильтрацией по номеру
    стола и статусу.
    """
    model = Order
    template_name = 'orders/order_list.html'

    def get_queryset(self):
        """
        Возвращает QuerySet заказов, отфильтрованных по GET-параметрам
        table_number и status.
        """
        try:
            qs = super().get_queryset()
            table = self.request.GET.get('table_number')
            status = self.request.GET.get('status')
            if table:
                qs = qs.filter(table_number=table)
            if status:
                qs = qs.filter(status=status)
            return qs
        except Exception:
            return Order.objects.none()

    def get_context_data(self, **kwargs):
        """
        Добавляет в контекст доступные статусы и текущие значения фильтров
        для шаблона.
        """
        ctx = super().get_context_data(**kwargs)
        try:
            ctx['statuses'] = Order.STATUS_CHOICES
            ctx['selected_table'] = self.request.GET.get('table_number', '')
            ctx['selected_status'] = self.request.GET.get('status', '')
            return ctx
        except Exception:
            ctx['error'] = 'Не удалось загрузить фильтр заказов'
            return ctx


class OrderUpdateView(UpdateView):
    """
    Представление для обновления статуса заказа.
    """
    model = Order
    fields = ['status']
    template_name = 'orders/order_update.html'
    success_url = reverse_lazy('order_list')


class OrderEditView(UpdateView):
    """
    Представление для полного редактирования заказа (номер стола, блюда,
     статус).
    После сохранения пересчитывает total_price.
    """
    model = Order
    form_class = OrderEditForm
    template_name = 'orders/order_update.html'
    success_url = reverse_lazy('order_list')

    def form_valid(self, form):
        """
        Пересчитывает total_price после редактирования заказа.
        """
        try:
            response = super().form_valid(form)
            self.object.total_price = self.object.calculate_total()
            self.object.save()
            return response
        except Exception as e:
            form.add_error(None, f"Ошибка при редактировании заказа")
            return self.form_invalid(form)


class RevenueView(TemplateView):
    """
    Представление для отображения отчета по выручке за смену.
    """
    template_name = 'orders/revenue.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        try:
            paid_qs = Order.objects.filter(status=ChoiceStatus.PAID)
            ctx['total_revenue'] = paid_qs.aggregate(total=Sum('total_price'))[
                                       'total'] or 0
            ctx['paid_orders'] = paid_qs
        except Exception:
            ctx['total_revenue'] = 0
            ctx['paid_orders'] = []
            ctx['error'] = "Не удалось загрузить выручку"
        return ctx
