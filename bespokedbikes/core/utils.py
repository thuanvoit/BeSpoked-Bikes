import datetime
import random

from django.db import connection
from .models import *

def execute_custom_query(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        data = cursor.fetchall()
    return data

def format_date(date):
    from datetime import datetime
    
    input_date = datetime.strptime(str(date), "%Y-%m-%d")
    return input_date.strftime("%Y-%m-%d")


def sale_calculate(price, discount_percentage, commission_percentage):
    
    discount_price = round((price * discount_percentage / 100), 2)
    final_price = round(float(price) - float(discount_price), 2)
    commission = round((price * commission_percentage / 100), 2)
    return {
        "sale_price": float(final_price),
        "discount": float(discount_price),
        "commission": float(commission)
    }


def get_apps_link():
    apps_link = [
        {"app_name": "Salesperson", "app_link": "core:salesperson",
            "app_info": "View all salespersons"},
        {"app_name": "Product", "app_link": "core:product",
            "app_info": "View all products"},
        {"app_name": "Customer", "app_link": "core:customer",
            "app_info": "View all customers"},
        {"app_name": "Sale", "app_link": "core:sale", "app_info": "View all sales"},
        {"app_name": "New Sale", "app_link": "core:new_sale",
            "app_info": "Make new sales"},
        {"app_name": "Sale Report", "app_link": "core:sale_report",
            "app_info": "Quarterly report"},
        {"app_name": "Sample", "app_link": "core:seed_sample",
            "app_info": "Seed Random Data"},
    ]
    return apps_link


def clean_data():
    customer = Customer.objects.all()
    customer.delete()
    salesperson = Salesperson.objects.all()
    salesperson.delete()
    product = Product.objects.all()
    product.delete()
    sale = Sale.objects.all()
    sale.delete()
    discount = Discount.objects.all()
    discount.delete()


def add_sample_data():
    generate_100_products()
    generate_100_customers()
    generate_100_salesperson()
    generate_50_salesperson_terminated()
    generate_discounts_for_products()
    generate_sample_sales()


def generate_100_products():
    for _ in range(100):
        name = "Product " + str(_)
        manufacturer = "Manufacturer " + str(_)
        # You can customize this as needed
        style = "Style " + str(random.randint(1, 10))
        purchase_price = round(random.uniform(10, 1000), 2)
        sale_price = round(purchase_price * random.uniform(1.1, 2.0), 2)
        qty_on_hand = random.randint(1, 100)
        commission_percentage = round(random.uniform(1, 10), 2)

        product = Product(
            name=name,
            manufacturer=manufacturer,
            style=style,
            purchase_price=purchase_price,
            sale_price=sale_price,
            qty_on_hand=qty_on_hand,
            commission_percentage=commission_percentage
        )
        product.save()


def generate_100_customers():
    first_names = ["Alice", "Bob", "Charlie", "David",
                   "Eva", "Frank", "Grace", "Helen", "Ivy", "Jack"]
    last_names = ["Smith", "Johnson", "Brown", "Lee",
                  "Davis", "Taylor", "Moore", "Hall", "Carter", "White"]

    for _ in range(100):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        address = f"{random.randint(1, 999)} {random.choice(['Main St', 'Elm St', 'Oak St'])}, City, AA, 20301"
        phone = f"555{random.randint(100, 999)}{random.randint(1000, 9999)}"

        start_date = datetime.date.today() - datetime.timedelta(days=random.randint(1,
                                                                                    3650))  # Random date within the last 10 years

        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone=phone,
            start_date=start_date
        )
        customer.save()


def generate_100_salesperson():
    first_names = []
    managers = []
    last_names = ["Smith", "Johnson", "Brown", "Lee",
                  "Davis", "Taylor", "Moore", "Hall", "Carter", "White"]

    for n in range(65, 91):
        first_names.append("Saler " + chr(n))
        managers.append("Manager " + chr(n))

    for _ in range(100):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        address = f"{random.randint(1, 999)} {random.choice(['Main St', 'Elm St', 'Oak St'])}, City, AA, 20301"
        phone = f"555{random.randint(100, 999)}{random.randint(1000, 9999)}"

        start_date = datetime.date.today(
        ) - datetime.timedelta(days=random.randint(1, 1825))  # last 5 years
        manager = random.choice(managers)

        salesperson = Salesperson(
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone=phone,
            start_date=start_date,
            manager=manager
        )
        salesperson.save()


def generate_50_salesperson_terminated():
    first_names = []
    managers = []
    last_names = ["Smith", "Johnson", "Brown", "Lee",
                  "Davis", "Taylor", "Moore", "Hall", "Carter", "White"]

    for n in range(65, 91):
        first_names.append("Saler " + chr(n))
        managers.append("Manager " + chr(n))

    for _ in range(50):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        address = f"{random.randint(1, 999)} {random.choice(['Main St', 'Elm St', 'Oak St'])}, City, AA, 20301"
        phone = f"555{random.randint(100, 999)}{random.randint(1000, 9999)}"

        start_date = datetime.date.today(
        ) - datetime.timedelta(days=random.randint(1, 1825))  # last 5 years

        termination_date = min(
            start_date + datetime.timedelta(days=random.randint(730, 1095)),
            datetime.date.today() 
        )

        manager = random.choice(managers)

        salesperson = Salesperson(
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone=phone,
            start_date=start_date,
            termination_date=termination_date,
            manager=manager
        )
        salesperson.save()


def generate_sample_sales():
    products = Product.objects.all()
    salespeople = Salesperson.objects.all()
    customers = Customer.objects.all()
    i = 0
    j = 0
    while i <= 300:
        product = random.choice(products)
        salesperson = random.choice(salespeople)
        customer = random.choice(customers)

        # Get the salesperson's start_date
        start_date = salesperson.start_date
        termination_date = salesperson.termination_date

        # Generate a random sales date within the range of start_date to today
        today = datetime.date.today()
        delta_days = (today - start_date).days

        if termination_date:
            sales_date = min(start_date + datetime.timedelta(days=random.randint(0, delta_days)),
                             termination_date)
        else:
            sales_date = start_date + \
                datetime.timedelta(days=random.randint(0, delta_days))

        # Generate a random sale price and salesperson commission

        discounts = Discount.objects.filter(
            product=product,
            begin_date__lte=sales_date,
            end_date__gte=sales_date,
        )
        max_discount = discounts.order_by('-discount_percentage').first()

        if discounts:
            product_price = sale_calculate(product.sale_price,
                                           max_discount.discount_percentage,
                                           product.commission_percentage)
            i += 1
        else:
            product_price = sale_calculate(product.sale_price,
                                           0,
                                           product.commission_percentage)
            j += 1
            if j >= 300:
                continue

        sale = Sale(
            product=product,
            salesperson=salesperson,
            customer=customer,
            sales_date=sales_date,
            price=product_price['sale_price'],
            salesperson_commission=product_price['commission'],
        )
        sale.save()


def generate_discounts_for_products():
    today = datetime.date.today()
    products = Product.objects.all()

    for product in products:
        for _ in range(random.randint(0, 2)):
            # Random start date within the last 5 years
            start_date = today - \
                datetime.timedelta(days=random.randint(0, 5 * 365))
            # Random end date within the next 3 months
            end_date = start_date + \
                datetime.timedelta(days=random.randint(1, 90))
            discount_percentage = random.choice([5, 10, 15, 20, 25, 30])

            discount = Discount(
                product=product,
                begin_date=start_date,
                end_date=end_date,
                discount_percentage=discount_percentage,
            )
            discount.save()
