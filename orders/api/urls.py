from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import OrderViewSet, RevenueAPIView, PracticeHandler

router = DefaultRouter()
router.register('orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('revenue/', RevenueAPIView.as_view(), name='api_revenue'),
    path('test/', PracticeHandler.as_view(), name='test'),
    path('practice/<int:pk>/', PracticeHandler.as_view(), name='practice_put')
]
