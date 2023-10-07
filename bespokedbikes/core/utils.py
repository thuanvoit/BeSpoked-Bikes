from .models import *

def format_date(date):
    from datetime import datetime
    input_date = datetime.strptime(str(date), "%Y-%m-%d")
    return input_date.strftime("%Y-%m-%d")

def add_sample_data():
    from datetime import date

    # Create Products
    product1 = Product.objects.create(
        name="Product A",
        manufacturer="Manufacturer X",
        style="Style 1",
        purchase_price=50.00,
        sale_price=100.00,
        qty_on_hand=100,
        commission_percentage=5.00,
    )

    product2 = Product.objects.create(
        name="Product B",
        manufacturer="Manufacturer Y",
        style="Style 2",
        purchase_price=40.00,
        sale_price=90.00,
        qty_on_hand=80,
        commission_percentage=4.50,
    )

    # Create Discounts
    discount1 = Discount.objects.create(
        product=product1,
        begin_date=date(2023, 1, 1),
        end_date=date(2023, 1, 31),
        discount_percentage=10.00,
    )

    discount2 = Discount.objects.create(
        product=product2,
        begin_date=date(2023, 2, 1),
        end_date=date(2023, 2, 28),
        discount_percentage=15.00,
    )

    # Create Customers
    customer1 = Customer.objects.create(
        first_name="John",
        last_name="Doe",
        address="123 Main St",
        phone="555-1234",
        start_date=date(2022, 5, 15),
    )

    customer2 = Customer.objects.create(
        first_name="Jane",
        last_name="Smith",
        address="456 Elm St",
        phone="555-5678",
        start_date=date(2023, 3, 10),
    )

    # Create Salespeople
    salesperson1 = Salesperson.objects.create(
        first_name="Alice",
        last_name="Johnson",
        address="789 Oak St",
        phone="555-1111",
        start_date=date(2022, 8, 20),
        manager="Manager X",
    )

    salesperson2 = Salesperson.objects.create(
        first_name="Bob",
        last_name="Williams",
        address="101 Pine St",
        phone="555-2222",
        start_date=date(2023, 1, 10),
        manager="Manager Y",
    )

    # Create Sales
    sale1 = Sale.objects.create(
        product=product1,
        salesperson=salesperson1,
        customer=customer1,
        sales_date=date(2023, 4, 5),
        price=90.00,
        salesperson_commission=4.50,
    )

    sale2 = Sale.objects.create(
        product=product2,
        salesperson=salesperson2,
        customer=customer2,
        sales_date=date(2023, 5, 12),
        price=75.00,
        salesperson_commission=3.75,
    )
    