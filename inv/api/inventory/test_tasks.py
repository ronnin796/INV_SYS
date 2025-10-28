from django.test import TestCase, override_settings
from django.core import mail
from django.contrib.auth import get_user_model
from api.inventory.models import Inventory
from api.product.models import Product
from api.category.models import Category
from api.subcategory.models import SubCategory
from api.suppliers.models import Supplier
from api.warehouse.models import Warehouse
from api.inventory.tasks import check_and_notify_low_stock

User = get_user_model()

@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class InventoryEmailTaskTest(TestCase):

    def setUp(self):
        # Create a user (manager)
        self.manager = User.objects.create_user(
            username="manager1", password="testpass123", email="manager1@example.com"
        )

        # Create category and subcategory
        self.category = Category.objects.create(name="Electronics")
        self.subcategory = SubCategory.objects.create(
            name="Laptops", category=self.category
        )

        # Create supplier
        self.supplier = Supplier.objects.create(
            name="Tech Supplier",
            contact_email="supplier@example.com",
            phone_number="9800000000",
            address="Kathmandu"
        )

        # Create products
        self.product_low = Product.objects.create(
            name="Laptop",
            price=1200.00,
            category=self.category,
            subcategory=self.subcategory,
            supplier=self.supplier
        )
        self.product_ok = Product.objects.create(
            name="Mouse",
            price=500.00,
            category=self.category,
            subcategory=self.subcategory,
            supplier=self.supplier
        )

        # Create warehouse
        self.warehouse = Warehouse.objects.create(
            name="Main Warehouse",
            location="Biratnagar",
            manager=self.manager
        )

        # Create inventories
        # Low-stock inventory
        self.inventory_low = Inventory.objects.create(
            warehouse=self.warehouse,
            product=self.product_low,
            quantity=3,  # Below reorder level
            reorder_level=5
        )
        # Normal stock inventory
        self.inventory_ok = Inventory.objects.create(
            warehouse=self.warehouse,
            product=self.product_ok,
            quantity=10,
            reorder_level=5
        )

    def test_low_stock_task_sends_email(self):
        """Check that low-stock inventory triggers email"""
        # Run the Celery task synchronously
        result = check_and_notify_low_stock()

        # Task should report emails sent
        self.assertIn("sent", result.lower())

        # One email should be in outbox
        self.assertEqual(len(mail.outbox), 1)

        # Verify email content
        email = mail.outbox[0]
        self.assertIn("Low Stock Alert", email.subject)
        self.assertIn("Laptop", email.body)  # Low-stock product
        self.assertNotIn("Mouse", email.body)  # Normal-stock product
        self.assertIn(self.manager.email, email.to)
    def test_no_email_when_all_stock_ok(self):
        """Check that no email is sent when all inventory is above reorder level"""
        # Update low-stock inventory to be above reorder level
        self.inventory_low.quantity = 6
        self.inventory_low.save()

        # Run the Celery task synchronously
        result = check_and_notify_low_stock()

        # Task should report zero emails sent
        self.assertIn("sent 0 alert emails", result.lower())

        # No emails should be in outbox
        self.assertEqual(len(mail.outbox), 0)