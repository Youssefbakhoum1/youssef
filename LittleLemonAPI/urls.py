from django.urls import path
from .views import MenuItemView, SingleMenuItemView, MenuItemSearchView, CustomAuthToken, manager_view

urlpatterns = [
    path('api-token-auth/', CustomAuthToken.as_view(), name='api-token-auth'),
    path('menu-items/', MenuItemView.as_view(), name='menuitem-list'),
    path('menu-items/<int:pk>/', SingleMenuItemView.as_view(), name='menuitem-detail'),
    path('menu-items/search/', MenuItemSearchView.as_view(), name='menuitem-search'),
    path('manager-view/', manager_view, name='manager-view'),  # Use the function-based view
]