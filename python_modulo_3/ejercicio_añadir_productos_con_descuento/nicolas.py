shopping_cart = []

DESCUENTO_PRODUCTO = 0.10  # 10% de descuento en productos individuales
DESCUENTO_TOTAL = 0.10     # 10% de descuento sobre total si > 100000

available_products = {
    "P1001": {"nombre": "Shampoo neutro", "precio_normal": 5000, "tiene_descuento": False},
    "P1002": {"nombre": "Limpiador de llantas", "precio_normal": 17500, "tiene_descuento": False},
    "P1003": {"nombre": "Cera líquida", "precio_normal": 22000, "tiene_descuento": True},
    "P1004": {"nombre": "Paño de microfibra", "precio_normal": 3000, "tiene_descuento": False},
    "P1005": {"nombre": "Desengrasante", "precio_normal": 16800, "tiene_descuento": False},
    "P1006": {"nombre": "Limpiavidrios", "precio_normal": 14200, "tiene_descuento": False},
    "P1007": {"nombre": "Acondicionador de cuero", "precio_normal": 15000, "tiene_descuento": True},
    "P1008": {"nombre": "Espuma activa", "precio_normal": 18900, "tiene_descuento": False},
    "P1009": {"nombre": "Cepillo detailing", "precio_normal": 12600, "tiene_descuento": False},
    "P1010": {"nombre": "Sellador cerámico", "precio_normal": 21000, "tiene_descuento": True}
}

continuar = "s"

while continuar.lower() == "s":

    print("\nProductos disponibles:\n")
    productos_lista = list(available_products.items())

    for i, (sku, producto) in enumerate(productos_lista, start=1):
        print(f"{i}. {producto['nombre']} - ${producto['precio_normal']}")

    opcion = int(input("\nIngrese el número del producto que desea comprar: "))

    sku_seleccionado, producto = productos_lista[opcion - 1]

    # Calculamos precio con descuento individual
    precio_final = producto["precio_normal"]
    if producto["tiene_descuento"]:
        precio_final *= (1 - DESCUENTO_PRODUCTO)

    shopping_cart.append({
        "sku": sku_seleccionado,
        "nombre": producto["nombre"],
        "precio": precio_final
    })

    print(f"\nProducto agregado: {producto['nombre']} - ${precio_final:.0f}")

    continuar = input("\n¿Desea agregar otro producto? (s/o): ")

# Calculamos total
total = sum(item["precio"] for item in shopping_cart)

# Aplicar descuento total si supera 100000
if total >= 100000:
    total = sum(item["precio"] for item in shopping_cart)  # ignoramos descuento individual
    total *= (1 - DESCUENTO_TOTAL)
    print("\nSe aplicó un 10% de descuento sobre el total (compra ≥ 100000)")

# Mostrar carrito final
print("\nCompra finalizada.")
print("Carrito de compras:")
for item in shopping_cart:
    print(f"- {item['nombre']} (${item['precio']:.0f})")

print(f"\nTotal a pagar: ${total:.0f}")