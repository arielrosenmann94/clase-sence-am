loads_amount = int(input("Cuántos productos desea cargar?: \n"))
product_info = {}

while loads_amount > 0:
    sku = input("Cuál es el SKU del producto?: \n")
    name_producto = input("Cuál es el nombre del producto?:\n")
    product_price = int(input("Cuál es el precio del producto?: \n"))
    product_info[sku] = {
        "nombre": name_producto,
        "precio": product_price
    }
    print("Producto cargado correctamente")
    loads_amount -= 1

print("Productos cargados:")
print(product_info)