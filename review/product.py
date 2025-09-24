class Product:
    def __init__(self, id  = None, name = None, quantity = None, price = None): #tu dong khoi tao gia tri cho thuoc tinh cua dt khi dt dc cap phat o nho
       self.id = id
       self.name = name
       self.quantity = quantity
       self.price = price
    def __str__(self):
        return f"{self.id}\t{self.name}\t{self.price}"