# Preguntar cuántos productos quiere cargar
products_quantity = int(input("¿Cuántos productos quiere cargar?: "))

# Diccionario para almacenar los productos
products = {}

# Cargar los productos
for i in range(products_quantity):
    print(f"\nProducto {i + 1}")
    
    product_sku = input("Ingrese el SKU del producto: ")
    product_name = input("Ingrese el nombre del producto: ")
    product_price = float(input("Ingrese el precio del producto: "))
    
    products[product_sku] = {
        "nombre": product_name,
        "precio": product_price
    }

# Imprimir en pantalla los productos cargados
print("\nProductos cargados:")
print(products)