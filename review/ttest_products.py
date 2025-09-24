from review.product import Product
from review.products import ListProducts

lp = ListProducts()
lp.add_product(Product(100, "Product 1", 200, 100))
lp.add_product(Product(200, "Product 2", 10, 15))
lp.add_product(Product(150, "Product 3", 80, 8))
lp.add_product(Product(300, "Product 4", 50, 20))
lp.add_product(Product(250, "Product 5", 150, 17))
print("List of products")
lp.print_products()
lp.desc_sort_product()
print(" List of Products after descending sort:")
lp.print_products()

lp.desc_sort_product2()
print(" List of Products after descending sort:")
lp.print_products()

