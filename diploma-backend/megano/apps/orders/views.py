from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from apps.goods.models import Product
from apps.basket.models import Basket

from .models import Order, OrderItem
from .serializers import OrderSerializer


class OrderView(APIView):
    """
    Представление работы с заказами.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        GET /orders

        Метод получения всех заказов.
        """
        try:
            orders = Order.objects.filter(customer=request.user)
            serializer = OrderSerializer(orders, context={'request': request}, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
    def post(self, request):
        """
        POST /orders

        Метод добавления заказа.
        """
        permission_classes = [permissions.IsAuthenticated]
        try:
            if not isinstance(request.data, list) or len(request.data) == 0:
                return Response(
                    {"error": "Expected non-empty list of products"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                order = Order.objects.get(
                    customer=request.user,
                    status='pending'
                    )
            except Order.DoesNotExist:
                order = Order.objects.create(
                    customer=request.user,
                )
            total_cost = 0
            for item_data in request.data:
                product_id = item_data.get('id')
                count = item_data.get('count')
                product = Product.objects.get(pk=product_id)
                if product.count < count:
                    return Response(
                        {"error": f"Invalid count for product {product_id}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    count=count,
                )
                total_cost += product.price * count
            if total_cost < 2000 and order.delivery_type != 'express':
                total_cost += 200
            elif order.delivery_type == 'express':
                total_cost += 500
            order.total_cost = total_cost
            order.save()
            serializer = OrderSerializer(order, context={'request': request})
            Basket.objects.filter(user=request.user).delete()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Product.DoesNotExist:
            return Response(
                {"error": f"Product with id {product_id} not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except KeyError as e:
            return Response(
                {"error": f"Missing field: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )


class OrderDetailView(APIView):
    """
    Представление работы с заказами по id.
    """
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id: int):
        """
        Метод получения заказа по id.

        Attributes:
            id(int): Id заказа.
        """
        try:
            order = Order.objects.get(pk=id)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

    def post(self, request, id: int):
        """
        POST /order/{id}

        Метод подтверждения заказа.

        Attributes:
            id(int): Id заказа.
        """
        permission_classes = [permissions.IsAuthenticated]
        try:
            order = Order.objects.get(pk=id)
            serializer = OrderSerializer(order, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )