# clientes_json_simple.py
import json

RUTA = "clientes.json"

# =========================
# CLASE CLIENTE
# =========================
class Cliente:
    campos = ["cliente_id", "nombre", "apellido", "email"]

    def __init__(self, **kwargs):
        for c in self.campos:
            setattr(self, c, kwargs.get(c))

    def a_dict(self):
        return {
            "cliente_id": self.cliente_id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email
        }


# =========================
# JSON
# =========================
def leer_json():
    try:
        with open(RUTA, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def guardar_json(data):
    with open(RUTA, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# =========================
# VALIDACIONES
# =========================
def pedir_entero(mensaje):
    while True:
        valor = input(mensaje)
        if valor.isdigit():
            return int(valor)
        print("Debe ingresar un número válido")


def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("El valor no puede estar vacío")


# =========================
# INGRESAR CLIENTE
# =========================
def ingresar_cliente():
    data = leer_json()

    cliente_id = pedir_entero("ID del cliente: ")
    nombre = pedir_texto("Nombre: ")
    apellido = pedir_texto("Apellido: ")
    email = pedir_texto("Email: ")

    cliente = Cliente(
        cliente_id=cliente_id,
        nombre=nombre,
        apellido=apellido,
        email=email
    )

    data.append(cliente.a_dict())
    guardar_json(data)

    print("\nCliente agregado correctamente:")
    print(cliente.a_dict())


# =========================
# EDITAR CLIENTE
# =========================
def editar_cliente():
    data = leer_json()

    if not data:
        print("No hay clientes registrados")
        return

    cliente_id = pedir_entero("ID del cliente a editar: ")

    for c in data:
        if c["cliente_id"] == cliente_id:

            print("\nSeleccione el campo a editar:")
            print("1. Nombre")
            print("2. Apellido")
            print("3. Email")

            opcion = pedir_entero("Opción: ")

            campos = {
                1: "nombre",
                2: "apellido",
                3: "email"
            }

            if opcion not in campos:
                print("Opción inválida")
                return

            nuevo_valor = pedir_texto("Nuevo valor: ")
            c[campos[opcion]] = nuevo_valor

            guardar_json(data)

            print("\nCliente modificado correctamente:")
            print(c)
            return

    print("Cliente no encontrado")


# =========================
# MENÚ
# =========================
while True:
    print("\n--- MENÚ CLIENTES ---")
    print("1. Ingresar cliente")
    print("2. Editar cliente")
    print("3. Salir")

    opcion = pedir_entero("Seleccione una opción: ")

    if opcion == 1:
        ingresar_cliente()
    elif opcion == 2:
        editar_cliente()
    elif opcion == 3:
        print("Saliendo del sistema...")
        break
    else:
        print("Opción inválida")