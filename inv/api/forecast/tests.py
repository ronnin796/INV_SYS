from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch
from django.contrib.auth import get_user_model

from api.inventory.models import Inventory
from api.product.models import Product
from api.category.models import Category
from api.subcategory.models import SubCategory
from api.suppliers.models import Supplier
from api.warehouse.models import Warehouse
from api.customer.models import Customer
from api.sales.models import SalesOrder, SalesItem
from api.forecast.models import ForecastResult
from api.forecast.services import evaluate_forecast, get_or_create_forecast

User = get_user_model()


class ForecastServiceTest(TestCase):
    def setUp(self):
        # Create a manager user
        self.manager = User.objects.create_user(username="manager1", password="pass123")

        # Create category/subcategory
        self.category = Category.objects.create(name="Electronics")
        self.subcategory = SubCategory.objects.create(name="Laptops", category=self.category)

        # Create supplier
        self.supplier = Supplier.objects.create(
            name="Tech Supplier",
            contact_email="supplier@example.com",
            phone_number="9800000000",
            address="Kathmandu"
        )

        # Create product
        self.product = Product.objects.create(
            name="Laptop",
            price=1200.0,
            category=self.category,
            subcategory=self.subcategory,
            supplier=self.supplier
        )

        # Create warehouse
        self.warehouse = Warehouse.objects.create(
            name="Main Warehouse",
            location="Kathmandu",
            manager=self.manager
        )

        # Create inventory
        self.inventory = Inventory.objects.create(
            warehouse=self.warehouse,
            product=self.product,
            quantity=20,
            reorder_level=10
        )

        # Create a dummy customer
        self.customer = Customer.objects.create(
            name="Test Customer",
            email="customer@example.com",
            phone="9800000000",
            created_by=self.manager
        )

        # Create sales order
        self.sales_order = SalesOrder.objects.create(
            warehouse=self.warehouse,
            status="Completed",
            created_at=timezone.now() - timedelta(days=1),
            customer=self.customer
        )

        # Create sales items
        for _ in range(5):
            SalesItem.objects.create(
                order=self.sales_order,
                product=self.product,
                quantity=2,
                price=1200.0
            )

    @patch("api.forecast.services.forecast_sales_for_product")
    def test_evaluate_forecast_returns_correct_structure(self, mock_forecast):
        """Test evaluate_forecast returns correct dictionary"""
        # Mock forecast_sales_for_product to return deterministic values
        mock_forecast.return_value = {
            "predicted_total_sales": 8,
            "forecast_series": [1, 2, 3]
        }

        result = evaluate_forecast(self.inventory, days_ahead=30)

        self.assertIsNotNone(result)
        self.assertEqual(result["product"], self.product)
        self.assertEqual(result["warehouse"], self.warehouse)
        self.assertEqual(result["predicted_sales"], 8)
        self.assertEqual(result["projected_stock"], self.inventory.quantity - 8)
        self.assertIn("will_be_low", result)
        self.assertIn("forecast_series", result)
        self.assertEqual(result["forecast_series"], [1, 2, 3])

    @patch("api.forecast.services.forecast_sales_for_product")
    def test_get_or_create_forecast_creates_and_caches(self, mock_forecast):
        """Test that get_or_create_forecast creates and caches ForecastResult"""
        mock_forecast.return_value = {
            "predicted_total_sales": 5,
            "forecast_series": [1, 1, 1]
        }

        # Initially, no forecast exists
        self.assertEqual(ForecastResult.objects.count(), 0)

        forecast = get_or_create_forecast(self.inventory, days_ahead=30)
        self.assertIsNotNone(forecast)
        self.assertEqual(ForecastResult.objects.count(), 1)
        self.assertEqual(forecast.projected_stock, self.inventory.quantity - 5)

        # Running again should return cached forecast
        forecast2 = get_or_create_forecast(self.inventory, days_ahead=30)
        self.assertEqual(forecast.id, forecast2.id)
        self.assertEqual(ForecastResult.objects.count(), 1)
