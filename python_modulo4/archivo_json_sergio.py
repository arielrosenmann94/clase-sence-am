import json
import os

class Cliente:
    '''
    Clase que representa la entidad Cliente. 
    Usa **kwargs para permitir una creación flexible y automatiza 
    la asignación de atributos mediante una lista de campos permitidos.
    '''
    campos = ["cliente_id", "nombre", "apellido", "email"]

    def __init__(self, **kwargs):
        for c in self.campos:
            setattr(self, c, kwargs.get(c))

    def a_dict(self):
        '''Convierte la instancia del objeto en un diccionario para ser guardado en JSON.'''
        return {c: getattr(self, c) for c in self.campos}


# --- FUNCIONES DE PERSISTENCIA (MANEJO DE DATOS) ---

def guardar_clientes_json(lista, ruta="clientes.json"):
    '''
    Toma una lista de objetos Cliente, los transforma a diccionarios
    y los sobreescribe en el archivo JSON especificado.
    '''
    data = [c.a_dict() for c in lista]
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def leer_clientes_json(ruta="clientes.json"):
    '''
    Lee el archivo JSON. Si el archivo no existe, retorna una lista vacía.
    Si existe, transforma cada diccionario de vuelta a un objeto tipo Cliente.
    '''
    if not os.path.exists(ruta):
        return []
    
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Reconstrucción de objetos: pasamos el diccionario como argumentos clave-valor
    return [Cliente(**d) for d in data]


def menu():
    '''
    Función principal con la ruta automatizada para evitar que 
    el JSON se guarde en carpetas inesperadas.
    '''
    # 1. Obtenemos la ruta absoluta del archivo .py actual
    ruta_script = os.path.abspath(__file__)
    
    # 2. Extraemos la carpeta donde está ese archivo
    directorio_actual = os.path.dirname(ruta_script)
    
    # 3. Creamos la ruta final uniendo la carpeta y el nombre del JSON
    ruta_archivo = os.path.join(directorio_actual, "clientes.json")
    
    # ... resto del código (el while True, etc.) ...
    
    while True:
        print("\n" + "="*20)
        print(" GESTIÓN DE CLIENTES")
        print("="*20)
        print("1. Agregar Cliente")
        print("2. Listar Clientes")
        print("3. Editar Cliente")
        print("4. Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            '''Lógica para capturar datos y agregar un nuevo registro'''
            clientes = leer_clientes_json(ruta_archivo)
            
            # Generamos un ID autoincremental simple
            nuevo_id = len(clientes) + 1
            
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            email = input("Correo: ")
            
            nuevo_cliente = Cliente(cliente_id=nuevo_id, nombre=nombre, apellido=apellido, email=email)
            clientes.append(nuevo_cliente)
            
            guardar_clientes_json(clientes, ruta_archivo)
            print(f"\n✅ Cliente '{nombre}' guardado con ID: {nuevo_id}")

        elif opcion == "2":
            '''Lógica para mostrar todos los clientes almacenados'''
            clientes = leer_clientes_json(ruta_archivo)
            if not clientes:
                print("\n⚠️ No hay clientes registrados.")
            else:
                print("\n--- LISTADO ACTUAL ---")
                for c in clientes:
                    print(f"ID: {c.cliente_id} | {c.nombre} {c.apellido} | Email: {c.email}")

        elif opcion == "3":
            '''Lógica para editar un campo específico buscando por ID'''
            try:
                c_id = input("Ingrese el ID del cliente a editar: ")
                campo = input("¿Qué campo desea editar (nombre/apellido/email)?: ").lower()
                nuevo_val = input(f"Ingrese el nuevo valor para {campo}: ")
                
                # Leemos los datos actuales
                clientes_actuales = leer_clientes_json(ruta_archivo)
                encontrado = False
                
                for c in clientes_actuales:
                    # Comparamos como string para evitar errores de tipo
                    if str(c.cliente_id) == str(c_id):
                        if hasattr(c, campo):
                            setattr(c, campo, nuevo_val)
                            encontrado = True
                            break
                
                if encontrado:
                    guardar_clientes_json(clientes_actuales, ruta_archivo)
                    print("✅ Cambio aplicado y guardado.")
                else:
                    print("❌ No se encontró un cliente con ese ID.")
                    
            except Exception as e:
                print(f"❌ Error durante la edición: {e}")

        elif opcion == "4":
            print("Cerrando sistema. ¡Adiós!")
            break
        else:
            print("⚠️ Opción inválida, intente de nuevo.")

if __name__ == "__main__":
    menu()