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

# Productos en oferta
productos_oferta = ["P1010", "P1007", "P1003"]

carrito = []
opcion = ""

print("=== TIENDA ===")
print("Productos disponibles:")
for producto in product_list:
    print(producto["sku"], "-", producto["nombre"], "- $", producto["precio"])

# Agregar productos al carrito
while opcion != "n":
    sku = input("\nIngrese SKU del producto a agregar: ").upper()
    encontrado = False

    for producto in product_list:
        if producto["sku"] == sku:
            carrito.append(producto)
            print("Producto agregado:", producto["nombre"])
            encontrado = True

    if not encontrado:
        print("SKU no válido")

    opcion = input("¿Desea agregar otro producto? (s/n): ").lower()

# Calcular totales
total_carrito = 0
total_descuento = 0

for producto in carrito:
    total_carrito += producto["precio"]

# Verificar si aplica descuento
if total_carrito > 100000:
    for producto in carrito:
        if producto["sku"] not in productos_oferta:
            total_descuento += producto["precio"] * 0.10

total_final = total_carrito - total_descuento

# Mostrar resumen
print("\n=== RESUMEN DE COMPRA ===")
for producto in carrito:
    print(producto["nombre"], "- $", producto["precio"])

print("\nTotal sin descuento: $", int(total_carrito))
print("Descuento aplicado: $", int(total_descuento))
print("Total a pagar: $", int(total_final))