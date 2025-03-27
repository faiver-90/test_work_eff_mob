from django.http import Http404
from rest_framework import viewsets, filters, status
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, ProtectedError

from orders.models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    API ViewSet для CRUD операций над моделью Order.
    Позволяет получать, создавать, обновлять и удалять заказы через REST API.
    Поддерживает поиск по полям table_number и status.
    """
    queryset = Order.objects.all().order_by('-id')
    serializer_class = OrderSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['table_number', 'status']

    def destroy(self, request, *args, **kwargs):
        try:
            order = self.get_object()
            self.perform_destroy(order)
            return Response({"message": "Заказ успешно удалён"},
                            status=status.HTTP_200_OK)
        except Http404:
            return Response({"error": "Заказ не найден"},
                            status=status.HTTP_404_NOT_FOUND)
        except ProtectedError:
            return Response(
                {"error": "Нельзя удалить заказ — имеются связанные записи"},
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise APIException(f"Внутренняя ошибка: {str(e)}")


class RevenueAPIView(APIView):
    """
    APIView для получения общей выручки (статус оплачено).
    GET-запрос возвращает JSON с полем total_revenue.
    """

    def get(self, request):
        try:
            total = Order.objects.filter(status=3).aggregate(
                sum=Sum('total_price'))['sum'] or 0
            return Response({'total_revenue': total})
        except Exception:
            return Response({'error': 'Не удалось рассчитать выручку'},
                            status=500)
