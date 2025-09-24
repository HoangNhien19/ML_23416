from review.product import Product

p1=Product(100, "Thuoc Ho", 4, 20)

print(p1)
p2 = Product(200, "Thuoc Paracetamol", 5, 30)
p1 = p2
print("Thông tin cua p1 =")
print(p1)
p1.name = "Thuoc tăng tự trọng"
print ("Thông tin của p2 =")
print(p2)