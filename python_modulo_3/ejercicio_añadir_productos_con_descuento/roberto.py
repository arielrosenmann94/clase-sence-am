# Lista de productos
product_list = [
    {"sku": "P1001", "nombre": "Audífonos Bluetooth", "precio": 24990},
    {"sku": "P1002", "nombre": "Teclado Mecánico", "precio": 44990},
    {"sku": "P1003", "nombre": "Mouse Gamer", "precio": 19990},
    {"sku": "P1004", "nombre": "Lámpara LED de Escritorio", "precio": 15990},
    {"sku": "P1005", "nombre": "Cargador Inalámbrico", "precio": 22990},
    {"sku": "P1006", "nombre": "Soporte para Notebook", "precio": 17990},
    {"sku": "P1007", "nombre": "Parlante Portátil", "precio": 29990},
    {"sku": "P1008", "nombre": "Cámara Web HD", "precio": 30990},
    {"sku": "P1009", "nombre": "Disco Duro Externo 500GB", "precio": 49990},
    {"sku": "P1010", "nombre": "Kit de Limpieza Electrónica", "precio": 10990},
]

# Productos en oferta (no aplica el 10% de descuento)
products_sale = ["P1010", "P1007", "P1003"]

# Carrito
cart = []

# Descuento
DISCOUNT = 0.1

# Totales
total = 0
total_sale = 0

# Ciclo principal del carrito
while True:
    while True:
        sku_input = input("\nIngrese el SKU del producto: ").upper()
        product_found = None

        for product in product_list:
            if product["sku"] == sku_input:
                product_found = product
                break

        if product_found:
            break
        else:
            print("SKU inválido. Intente nuevamente.")

    quantity = int(input("Ingrese la cantidad: "))

    # Agregar producto al carrito según cantidad
    for i in range(quantity):
        cart.append(product_found)
        total += product_found["precio"]

    add = input("¿Desea agregar otro producto? (s/n): ").lower()
    if add != "s":
        break

# Calcular total con descuento si aplica
if total > 100000:
    for product in cart:
        if product["sku"] in products_sale:
            total_sale += product["precio"]
        else:
            total_sale += product["precio"] * (1 - DISCOUNT)
else:
    total_sale = total

# Mostrar resultados
print("\nResumen del carrito:")
for product in cart:
    print(f"{product['sku']} - {product['nombre']} - ${product['precio']}")

print(f"\nTotal sin descuento: ${int(total)}")
print(f"Total a pagar: ${int(total_sale)}")