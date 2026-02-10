import json
import os
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict


# =========================
# 1) MODELOS (POO) MODELS
# =========================

@dataclass
class Persona:
    nombre: str
    apellido: str

    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}".strip()


@dataclass
class Cliente(Persona):
    correo: str
    cliente_id: int

    def actualizar(self, **kwargs):
        """
        Actualiza dinámicamente los atributos del cliente
        usando setattr + kwargs.get(c)
        """
        campos_validos = ["nombre", "apellido", "correo"]

        for c in campos_validos:
            valor = kwargs.get(c)

            if valor is None:
                continue

            if isinstance(valor, str):
                valor = valor.strip()
                if not valor:
                    continue

            if c == "correo":
                valor = valor.lower()

            setattr(self, c, valor)


# =========================
# 2) REPOSITORIO JSON
# =========================

class RepositorioClientesJSON:
    def __init__(self, ruta_archivo: str):
        self.ruta = ruta_archivo

    def cargar(self) -> Dict:
        if not os.path.exists(self.ruta):
            return {"ultimo_id": 0, "clientes": []}

        try:
            with open(self.ruta, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"ultimo_id": 0, "clientes": []}

    def guardar(self, data: Dict) -> None:
        with open(self.ruta, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


# =========================
# 3) GESTOR DE CLIENTES
# =========================

class GestorClientes:
    def __init__(self, repo: RepositorioClientesJSON):
        self.repo = repo
        self._data = self.repo.cargar()
        self.clientes: List[Cliente] = self._cargar_clientes()

    def _cargar_clientes(self) -> List[Cliente]:
        lista = []
        for c in self._data.get("clientes", []):
            lista.append(
                Cliente(
                    nombre=c["nombre"],
                    apellido=c["apellido"],
                    correo=c["correo"],
                    cliente_id=c["cliente_id"]
                )
            )
        return lista

    def _guardar(self):
        self._data["clientes"] = [asdict(c) for c in self.clientes]
        self.repo.guardar(self._data)

    def _nuevo_id(self) -> int:
        self._data["ultimo_id"] += 1
        return self._data["ultimo_id"]

    # -------- CRUD --------

    def crear_cliente(self, nombre: str, apellido: str, correo: str) -> Cliente:
        if not nombre.strip() or not apellido.strip():
            raise ValueError("Nombre y apellido son obligatorios")

        correo = correo.strip().lower()
        if "@" not in correo:
            raise ValueError("Correo inválido")

        cliente = Cliente(
            nombre=nombre.strip(),
            apellido=apellido.strip(),
            correo=correo,
            cliente_id=self._nuevo_id()
        )

        self.clientes.append(cliente)
        self._guardar()
        return cliente

    def listar(self) -> List[Cliente]:
        return self.clientes

    def buscar_por_id(self, cliente_id: int) -> Optional[Cliente]:
        for c in self.clientes:
            if c.cliente_id == cliente_id:
                return c
        return None

    def editar_cliente(self, cliente_id: int, **kwargs):
        cliente = self.buscar_por_id(cliente_id)
        if not cliente:
            raise ValueError("Cliente no encontrado")

        cliente.actualizar(**kwargs)
        self._guardar()

    def eliminar_cliente(self, cliente_id: int):
        self.clientes = [c for c in self.clientes if c.cliente_id != cliente_id]
        self._guardar()

# =========================
# 4) INTERFAZ POR CONSOLA
# =========================

def main():
    repo = RepositorioClientesJSON("clientes.json")
    gestor = GestorClientes(repo)

    while True:
        print("\n=== SISTEMA DE CLIENTES ===")
        print("1. Agregar cliente")
        print("2. Ver clientes")
        print("3. Editar cliente")
        print("4. Eliminar cliente")
        print("0. Salir")

        opcion = input("Seleccione opción: ")

        try:
            if opcion == "1":
                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                correo = input("Correo: ")
                c = gestor.crear_cliente(nombre, apellido, correo)
                print(f"✔ Cliente creado: {c.cliente_id} - {c.nombre_completo()}")

            elif opcion == "2":
                print("\n--- CLIENTES ---")
                for c in gestor.listar():
                    print(f"{c.cliente_id} - {c.nombre_completo()} | {c.correo}")

            elif opcion == "3":
                cid = int(input("ID del cliente: "))
                print("Deja vacío para no cambiar")

                nombre = input("Nuevo nombre: ").strip() or None
                apellido = input("Nuevo apellido: ").strip() or None
                correo = input("Nuevo correo: ").strip() or None

                gestor.editar_cliente(
                    cid,
                    nombre=nombre,
                    apellido=apellido,
                    correo=correo
                )
                print("✔ Cliente actualizado")

            elif opcion == "4":
                cid = int(input("ID del cliente: "))
                gestor.eliminar_cliente(cid)
                print("✔ Cliente eliminado")

            elif opcion == "0":
                print("Chao 👋")
                break

            else:
                print("Opción inválida")

        except ValueError as e:
            print(f"❌ Error: {e}")


# main.py
if __name__ == "__main__":
    main()