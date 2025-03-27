from rest_framework import viewsets, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum

from orders.models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-id')
    serializer_class = OrderSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['table_number', 'status']

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        self.perform_destroy(order)
        return Response(
            {"message": f"Заказ успешно удалён"},
            status=status.HTTP_200_OK
        )


class RevenueAPIView(APIView):
    def get(self, request):
        total = \
            Order.objects.filter(status=3).aggregate(sum=Sum('total_price'))[
                'sum'] or 0
        return Response({'total_revenue': total})
