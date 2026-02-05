# clientes_json_editable.py
import json

class Cliente:
    campos = ["cliente_id", "nombre", "email"]

    def __init__(self, **kwargs):
        for c in self.campos:
            setattr(self, c, kwargs.get(c))

    def a_dict(self):
        return {
            "cliente_id": self.cliente_id,
            "nombre": self.nombre,
            "email": self.email,
        }


def guardar_clientes_json(**kwargs):
    ruta = kwargs.get("ruta") or "clientes.json"
    lista = kwargs.get("lista")
    if lista is None:
        raise ValueError("Falta 'lista'")

    data = [c.a_dict() for c in lista]

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return ruta


def leer_clientes_json(**kwargs):
    ruta = kwargs.get("ruta")
    if ruta is None:
        raise ValueError("Falta 'ruta'")

    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)

    clientes = []
    for d in data:
        clientes.append(Cliente(cliente_id=d.get("cliente_id"), nombre=d.get("nombre"), email=d.get("email")))

    return clientes


def editar_campo_por_id_json(**kwargs):
    ruta = kwargs.get("ruta")
    cliente_id = kwargs.get("cliente_id")
    campo = kwargs.get("campo")          # "nombre" o "email" (o más claves)
    nuevo_valor = kwargs.get("nuevo_valor")

    if ruta is None or cliente_id is None or campo is None or nuevo_valor is None:
        raise ValueError("Falta 'ruta', 'cliente_id', 'campo' o 'nuevo_valor'")

    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)

    encontrado = False
    for d in data:
        if int(d.get("cliente_id")) == int(cliente_id):
            if campo not in d:
                raise ValueError(f"Campo inválido: {campo}. Claves: {list(d.keys())}")
            d[campo] = nuevo_valor
            encontrado = True
            break

    if not encontrado:
        raise ValueError(f"No existe cliente_id={cliente_id}")

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return True


# -------- DEMO --------
clientes = [
    Cliente(cliente_id=1, nombre="Carla", email="carla@mimail.cl"),
    Cliente(cliente_id=2, nombre="Josefa", email="josefa@miempresa.cl"),
]

ruta = guardar_clientes_json(lista=clientes, ruta="clientes.json")
print("OK: json creado en", ruta)

editar_campo_por_id_json(ruta="clientes.json", cliente_id=2, campo="nombre", nuevo_valor="Josefa Andrea")
editar_campo_por_id_json(ruta="clientes.json", cliente_id=1, campo="email", nuevo_valor="carla@nuevo.cl")
print("OK: cambios aplicados")

for c in leer_clientes_json(ruta="clientes.json"):
    print(c.a_dict())
