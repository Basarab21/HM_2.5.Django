from django.http import HttpResponse
from .models import Product
import random

NAMES = ["Футболка", "Куртка", "Джинси", "Светр", "Сорочка", "Шорти", "Сукня", "Спідниця"]
BRANDS = ["Nike", "Adidas", "Zara", "H&M", "Puma", "Reserved", "Gant", "Levis"]
SIZES = ["XS", "S", "M", "L", "XL"]
COLORS = ["Червоний", "Синій", "Чорний", "Білий", "Сірий", "Зелений", "Жовтий"]


def products_list_view(request):
    products = Product.objects.all()

    html_table = """
    <!DOCTYPE html>
    <html>
    <head><title>Склад Одягу</title></head>
    <body>
    <h2>Список товарів (Одяг)</h2>
    <p>Для поповнення складу додайте до URL-адреси /replenish/N, де N - кількість (наприклад, <a href="/replenish/5/">/replenish/5/</a>).</p>
    <table border="1" style="border-collapse: collapse; width: 80%;">
        <tr style="background-color: #f2f2f2;">
            <th>ID</th>
            <th>Назва</th>
            <th>Бренд</th>
            <th>Розмір</th>
            <th>Колір</th>
            <th>Ціна</th>
        </tr>
    """

    for product in products:
        html_table += f"""
        <tr>
            <td>{product.id}</td>
            <td>{product.name}</td>
            <td>{product.brand}</td>
            <td>{product.size}</td>
            <td>{product.color}</td>
            <td>{product.price} грн</td>
        </tr>
        """

    html_table += "</table>"
    html_table += f"<p>Всього товарів на складі: <strong>{products.count()}</strong></p>"
    html_table += "</body></html>"

    return HttpResponse(html_table)


def replenish_view(request, count):

    if count <= 0:
        return HttpResponse("Кількість товарів для поповнення має бути додатним числом.", status=400)

    products_to_create = []

    for _ in range(count):
        product = Product(
            name=random.choice(NAMES),
            brand=random.choice(BRANDS),
            size=random.choice(SIZES),
            color=random.choice(COLORS),
            price=round(random.uniform(200.0, 3000.0), 2)
        )
        products_to_create.append(product)

    Product.objects.bulk_create(products_to_create)
    response_text = f"Додано {count} нових записів одягу до складу. <p><a href='/products/'>Перейти до списку товарів</a></p>"

    return HttpResponse(response_text)