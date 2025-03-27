from django.urls import path

from . import views
from .views import CreateOrder, DeleteOrder, OrderListView, OrderUpdateView, \
    RevenueView, OrderEditView

urlpatterns = [
    path("", views.index, name="index"),
    path("create_order/", CreateOrder.as_view(), name="create_order"),
    path("<int:pk>/delete/", DeleteOrder.as_view(), name="delete_order"),
    path("order_list/", OrderListView.as_view(), name="order_list"),
    path("<int:pk>/update_status/", OrderUpdateView.as_view(),
         name="update_status"),
    path("revenue/", RevenueView.as_view(), name="order_revenue"),
    path("<int:pk>/edit/", OrderEditView.as_view(), name="order_edit"),
]
