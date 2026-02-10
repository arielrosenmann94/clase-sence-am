import json
import os

# --- CLASES (POO) ---
class Cliente:
    def __init__(self, nombre, apellido, correo):
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo

    def to_dict(self):
        return {"nombre": self.nombre, "apellido": self.apellido, "correo": self.correo}

class GestorClientes:
    def __init__(self, archivo='clientes.json'):
        self.archivo = archivo
        self.clientes = self.cargar_datos()

    def cargar_datos(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except: return []
        return []

    def guardar_datos(self):
        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump(self.clientes, f, indent=4, ensure_ascii=False)

    def agregar(self, n, a, c):
        nuevo = Cliente(n, a, c)
        self.clientes.append(nuevo.to_dict())
        self.guardar_datos()

    def editar(self, indice, n, a, c):
        if 0 <= indice < len(self.clientes):
            if n: self.clientes[indice]['nombre'] = n
            if a: self.clientes[indice]['apellido'] = a
            if c: self.clientes[indice]['correo'] = c
            self.guardar_datos()
            return True
        return False

# --- INTERFAZ DE USUARIO ---
def ejecutar():
    gestor = GestorClientes()
    
    while True:
        print(f"\n--- GESTIÓN DE CLIENTES ({len(gestor.clientes)} registrados) ---")
        print("1. Registrar nuevo")
        print("2. Ver lista / Editar")
        print("3. Salir")
        
        op = input("Seleccione: ")

        if op == "1":
            nom = input("Nombre: ")
            ape = input("Apellido: ")
            cor = input("Correo: ")
            gestor.agregar(nom, ape, cor)
            print("✅ Guardado.")

        elif op == "2":
            for i, cl in enumerate(gestor.clientes):
                print(f"[{i}] {cl['nombre']} {cl['apellido']} - {cl['correo']}")
            
            op_edit = input("\n¿Desea editar alguno? (S/N): ").lower()
            if op_edit == 's':
                idx = int(input("Ingrese el número del índice: "))
                print("(Deje vacío para no cambiar el dato actual)")
                n = input("Nuevo nombre: ")
                a = input("Nuevo apellido: ")
                c = input("Nuevo correo: ")
                if gestor.editar(idx, n, a, c):
                    print("🔄 Cliente actualizado.")
                else:
                    print("❌ Error: Índice no encontrado.")

        elif op == "3":
            print("👋 ¡Hasta luego!")
            break

if __name__ == "__main__":
    ejecutar()