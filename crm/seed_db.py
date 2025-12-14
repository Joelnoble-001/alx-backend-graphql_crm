import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_graphql_crm.settings")
django.setup()

from crm.models import Customer, Product

Customer.objects.bulk_create([
    Customer(name="Alice", email="alice@example.com"),
    Customer(name="Bob", email="bob@example.com")
])

Product.objects.bulk_create([
    Product(name="Laptop", price=999.99, stock=10),
    Product(name="Phone", price=499.99, stock=20)
])

print("Database seeded!")
