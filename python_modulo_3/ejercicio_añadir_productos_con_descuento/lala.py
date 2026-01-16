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

productos_oferta = ["P1010", "P1007", "P1003"]

carrito = []
total = 0
total_descuento = 0

print("Lista de productos disponibles:")
for producto in product_list:
    print(producto["sku"], "-", producto["nombre"], "- $", producto["precio"])

cantidad = int(input("\n¿Cuántos productos desea agregar al carrito?: "))

contador = 1

while contador <= cantidad:
    sku_ingresado = input("Ingrese el SKU del producto: ")

    for producto in product_list:
        if producto["sku"] == sku_ingresado:
            carrito.append(producto)
            total = total + producto["precio"]

            if sku_ingresado not in productos_oferta:
                total_descuento = total_descuento + producto["precio"]

    contador = contador + 1

print("\nProductos en el carrito:")
for item in carrito:
    print(item["nombre"], "- $", item["precio"])

print("\nTotal sin descuento: $", total)

if total > 100000:
    descuento = total_descuento * 0.10
    total_final = total - descuento
    print("Descuento aplicado: $", int(descuento))
else:
    total_final = total
    print("No se aplica descuento")

print("Total a pagar: $", int(total_final))