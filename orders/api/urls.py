from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import OrderViewSet, RevenueAPIView

router = DefaultRouter()
router.register('orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('revenue/', RevenueAPIView.as_view(), name='api_revenue'),
]
