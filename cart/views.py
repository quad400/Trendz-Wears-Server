from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound,ValidationError

from product.models import Product
from .models import Cart
from .serializers import CartSerializer

class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        id = kwargs["pk"]
        user = request.user
        product = Product.objects.filter(id=id)
        try:
            if product.exists():
                cart = Cart.objects.filter(cart_product=product[0])
                if cart.exists():
            
                    return Response({
                        "message": "Product is already added"
                    }, status=status.HTTP_302_FOUND)
                serializer = CartSerializer(data=request.data)
                if not serializer.is_valid():
                    raise ValidationError("Cart details is not valid", status.HTTP_400_BAD_REQUEST)
                serializer.save(cart_product=product[0], user=user)
            
                return Response({"message": "Sucessfully added product to cart"}, status=status.HTTP_200_OK)
            
            return Response({"message": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except NotFound:
            raise Response({"message": "Product does not exists"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, *ars, **kwargs):
        user = request.user
        cart = Cart.objects.filter(user=user)
        if cart.exists():
            serializer = CartSerializer(instance=cart, many=True).data
            return Response(serializer, status=status.HTTP_200_OK)
        return Response({"message": "User has no product in cart"}, status=status.HTTP_200_OK)
    

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_product_from_cart(request, *args, **kwargs):
    id = kwargs["pk"]
    user = request.user
    cart = Cart.objects.filter(user=user, id=id)
    try:
        if cart.exists():
            cart.delete()
            return Response({"message": "Successfully remove product from cart"}, status=status.HTTP_200_OK)
        return Response({"message": "Product is not in cart"})
    
    except NotFound:
            raise Response({"message": "Cart does not exists"}, status=status.HTTP_404_NOT_FOUND)