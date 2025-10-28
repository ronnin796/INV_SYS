from django.test import TestCase
from api.inventory.models import Inventory
from api.product.models import Product
from api.category.models import Category
from api.subcategory.models import SubCategory
from api.suppliers.models import Supplier
from api.warehouse.models import Warehouse
from django.contrib.auth import get_user_model

class InventoryModelTest(TestCase):

    def setUp(self):
        # Create a user (warehouse manager)
        User = get_user_model()
        self.user = User.objects.create_user(
            username="manager1", password="testpass123"
        )

        # Create category and subcategory
        self.category = Category.objects.create(name="Electronics")
        self.subcategory = SubCategory.objects.create(
            name="Laptops", category=self.category
        )

        # Create supplier (✅ fixed field names)
        self.supplier = Supplier.objects.create(
            name="Tech Supplier",
            contact_email="supplier@example.com",
            phone_number="9800000000",
            address="Kathmandu"
        )

        # Create product linked to category, subcategory, and supplier
        self.product = Product.objects.create(
            name="Laptop",
            price=1200.00,
            category=self.category,
            subcategory=self.subcategory,
            supplier=self.supplier
        )

        # Create warehouse
        self.warehouse = Warehouse.objects.create(
            name="Main Warehouse",
            location="Biratnagar",
            manager=self.user
        )

        # Create inventory entry
        self.inventory = Inventory.objects.create(
            warehouse=self.warehouse,
            product=self.product,
            quantity=5,
            reorder_level=10
        )

    def test_inventory_below_reorder(self):
        """Check if is_below_reorder property works"""
        self.assertTrue(self.inventory.is_below_reorder)

    def test_inventory_restock(self):
        """Test restock() increases quantity correctly"""
        self.inventory.restock(10)
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.quantity, 15)

    def test_inventory_str(self):
        """Test __str__ representation"""
        expected_str = f"{self.product.name} - {self.warehouse.name}"
        self.assertEqual(str(self.inventory), expected_str)


