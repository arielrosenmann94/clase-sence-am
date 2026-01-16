productos_oferta = ["P1010", "P1007", "P1003"]

carrito = []
total = 0
total_descuento = 0

cantidad = int(input("¿Cuántos productos desea agregar al carrito? "))

for i in range(cantidad):
    print(f"\nProducto {i + 1}")
    sku = input("Ingrese el SKU: ")
    precio = int(input("Ingrese el precio del producto: "))

    carrito.append((sku, precio))
    total += precio

# Aplicar descuento si supera 100.000
if total > 100000:
    for producto in carrito:
        sku = producto[0]
        precio = producto[1]

        if sku not in productos_oferta:
            total_descuento += precio * 0.10

total_final = total - total_descuento

print("\nResumen del carrito:")
for producto in carrito:
    print(f"SKU: {producto[0]} | Precio: ${producto[1]}")

print(f"\nTotal sin descuento: ${total}")
print(f"Descuento aplicado: ${int(total_descuento)}")
print(f"Total a pagar: ${int(total_final)}")



