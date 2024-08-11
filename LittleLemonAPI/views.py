from rest_framework import generics, filters, status
from django_filters import rest_framework as django_filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.authentication import TokenAuthentication

from .models import MenuItem
from .serializers import MenuItemSerializer
from .filters import MenuItemFilter

# Custom view for obtaining an authentication token
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

# View for listing and creating menu items
class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = MenuItemFilter
    search_fields = ['title']
    ordering_fields = ['title', 'price', 'inventory']
    ordering = ['title']
    permission_classes = [IsAuthenticated]  # Enforce authentication

# View for retrieving, updating, and deleting a single menu item
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]  # Enforce authentication

# View for searching menu items
class MenuItemSearchView(APIView):
    permission_classes = [IsAuthenticated]  # Enforce authentication

    def get(self, request, *args, **kwargs):
        title = request.query_params.get('title', None)
        price_min = request.query_params.get('price_min', None)
        price_max = request.query_params.get('price_max', None)

        queryset = MenuItem.objects.all()
        
        if title:
            queryset = queryset.filter(title__icontains=title)
        
        if price_min is not None:
            queryset = queryset.filter(price__gte=price_min)
        
        if price_max is not None:
            queryset = queryset.filter(price__lte=price_max)
        
        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 3  # Set the page size to 3 items per page
        page = paginator.paginate_queryset(queryset, request)
        
        if page is not None:
            serializer = MenuItemSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        # If no pagination applied (fallback), serialize and return the full queryset
        serializer = MenuItemSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)