from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import MenuItem, Category

class MenuItemFilterTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test categories
        cls.category1 = Category.objects.create(title='Starters', slug='starters')
        cls.category2 = Category.objects.create(title='Main Courses', slug='main-courses')
        
        # Create test MenuItems
        cls.item1 = MenuItem.objects.create(title='Salad', price=5.00, inventory=10, category=cls.category1)
        cls.item2 = MenuItem.objects.create(title='Pasta', price=10.00, inventory=15, category=cls.category2)
        cls.item3 = MenuItem.objects.create(title='Soup', price=7.00, inventory=8, category=cls.category1)
        cls.item4 = MenuItem.objects.create(title='Steak', price=15.00, inventory=5, category=cls.category2)

    def test_filter_by_title(self):
        url = reverse('menuitem-list')
        response = self.client.get(url, {'title': 'Salad'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Salad')

    def test_filter_by_price_min(self):
        url = reverse('menuitem-list')
        response = self.client.get(url, {'price_min': 8.00})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Expecting Pasta and Steak

    def test_filter_by_price_max(self):
        url = reverse('menuitem-list')
        response = self.client.get(url, {'price_max': 8.00})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Expecting Salad and Soup

    def test_filter_by_price_range(self):
        url = reverse('menuitem-list')
        response = self.client.get(url, {'price_min': 5.00, 'price_max': 10.00})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Expecting Salad, Soup, and Pasta

    def test_filter_by_title_and_price(self):
        url = reverse('menuitem-list')
        response = self.client.get(url, {'title': 'Soup', 'price_max': 8.00})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Soup')
