from django.urls import path

from . import views
from .views import CreateOrder, DeleteOrder, OrderListView, OrderUpdateView

urlpatterns = [
    path("", views.index, name="index"),
    path("create_order/", CreateOrder.as_view(), name="create_order"),
    path("<int:pk>/delete/", DeleteOrder.as_view(), name="delete_order"),
    path("orders/", OrderListView.as_view(), name="order_list"),
    path("<int:pk>/update_status/", OrderUpdateView.as_view(),
         name="update_status"),

]
