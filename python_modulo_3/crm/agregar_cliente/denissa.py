# ===================================
# CRM PARA TERAPEUTAS - VERSIÓN BÁSICA
# Gestión de Pacientes sin Funciones
# ===================================

pacientes = [] #base de datos 
ultimo_id = 0 #declaracion de la variable 

#usamos Switch.py, otra opcion seria usar match case necesita otra funcion que tome el diccionario, es variable,  dependiendo de la naturaleza del programa en django en "choice"
estados_paciente = {
    1: "Paciente potencial",
    2: "Paciente con alto interés",
    3: "En proceso de compra",
    4: "Cliente efectivo",
    5: "Super cliente"
}

print(
    "=" * 50 + "\n"
    "    SISTEMA CRM PARA TERAPEUTAS\n"
    "    Gestión de Pacientes\n"
    + "=" * 50
)

# --- MENÚ PRINCIPAL ---
while True:
    print(
        "\n--- MENÚ PRINCIPAL ---\n"
        "1. Agregar nuevo paciente\n"
        "2. Ver todos los pacientes\n"
        "3. Salir"
    )

    opcion = input("\nSelecciona una opción (1-3): ")

    # ============================
    # OPCIÓN 1: AGREGAR PACIENTE
    # ============================
    if opcion == "1":
        print(
            "\n" + "=" * 50 + "\n"
            "REGISTRAR NUEVO PACIENTE\n"
            + "=" * 50
        )

        print("\nSelecciona el tipo de paciente:")
        for clave, valor in estados_paciente.items():
            print(f"{clave}. {valor}")

        tipo_paciente = input("\nIngresa el número (1-5): ")

        if tipo_paciente.isdigit():
            tipo_paciente = int(tipo_paciente)

            if tipo_paciente in estados_paciente:
                ultimo_id += 1

                print(
                    f"\nRegistrando paciente como: {estados_paciente[tipo_paciente]}\n"
                    + "-" * 50
                )

                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                
                # =============================
                # VALIDACIÓN DE RUT CHILENO
                # =============================
                rut_valido = False
                while not rut_valido:
                    rut = input("RUT (formato: 12345678-9): ")
                    
                    # Verificar formato básico: debe tener un guión
                    if "-" in rut:
                        partes = rut.split("-")
                        # Verificar que tenga 2 partes
                        if len(partes) == 2:
                            numero = partes[0]
                            digito = partes[1]
                            # Verificar que el número sea dígitos y el dígito sea válido
                            if numero.isdigit() and len(numero) >= 7 and len(numero) <= 8:
                                if digito.isdigit() or digito.upper() == "K":
                                    rut_valido = True
                                else:
                                    print("✗ El dígito verificador debe ser un número o 'K'")
                            else:
                                print("✗ El número debe tener entre 7 y 8 dígitos")
                        else:
                            print("✗ Formato inválido. Usa el formato: 12345678-9")
                    else:
                        print("✗ Debes incluir el guión. Ejemplo: 12345678-9")
                
                # =============================
                # VALIDACIÓN DE TELÉFONO CHILENO
                # =============================
                telefono_valido = False
                while not telefono_valido:
                    telefono = input("Teléfono (formato: +56912345678 o 912345678): ")
                    
                    # Remover espacios
                    telefono = telefono.replace(" ", "")
                    
                    # Caso 1: Con código país +56
                    if telefono.startswith("+56"):
                        numero_sin_codigo = telefono[3:]  # Quita +56
                        if numero_sin_codigo.isdigit() and len(numero_sin_codigo) == 9:
                            telefono_valido = True
                        else:
                            print("✗ Después de +56 deben ir 9 dígitos (ej: +56912345678)")
                    # Caso 2: Sin código país (debe empezar con 9)
                    elif telefono.isdigit() and len(telefono) == 9 and telefono[0] == "9":
                        telefono_valido = True
                    else:
                        print("✗ Formato inválido. Usa +56912345678 o 912345678")
                
                # =============================
                # VALIDACIÓN DE CORREO ÚNICO
                # =============================
                correo_valido = False
                while not correo_valido:
                    correo = input("Correo electrónico: ")
                    
                    # Validar formato básico (debe tener @ y un punto después)
                    if "@" in correo and "." in correo.split("@")[1]:
                        # Verificar que no exista en la base de datos
                        correo_existe = False
                        for paciente in pacientes:
                            if paciente["correo"].lower() == correo.lower():
                                correo_existe = True
                                break
                        
                        if correo_existe:
                            print(f"✗ Error: El correo '{correo}' ya está registrado")
                        else:
                            correo_valido = True
                    else:
                        print("✗ Formato de correo inválido. Debe contener @ y dominio (ej: ejemplo@correo.com)")

                nuevo_paciente = {
                    "id": ultimo_id,
                    "nombre": nombre,
                    "apellido": apellido,
                    "rut": rut,
                    "telefono": telefono,
                    "correo": correo,
                    "estado": estados_paciente[tipo_paciente]
                }

                pacientes.append(nuevo_paciente)

                print(
                    "\n✓ ¡Paciente registrado exitosamente!\n"
                    f"ID asignado: {ultimo_id}"
                )
            else:
                print("\n✗ Error: Tipo de paciente no válido")
        else:
            print("\n✗ Error: Debes ingresar un número válido")

    # ============================
    # OPCIÓN 2: VER PACIENTES
    # ============================
    elif opcion == "2":
        print(
            "\n" + "=" * 50 + "\n"
            "LISTA DE PACIENTES REGISTRADOS\n"
            + "=" * 50
        )

        if len(pacientes) == 0:
            print("\nNo hay pacientes registrados aún.")
        else:
            for paciente in pacientes:
                print(
                    f"\nID: {paciente['id']}\n"
                    f"Nombre: {paciente['nombre']} {paciente['apellido']}\n"
                    f"RUT: {paciente['rut']}\n"
                    f"Teléfono: {paciente['telefono']}\n"
                    f"Correo: {paciente['correo']}\n"
                    f"Estado: {paciente['estado']}\n"
                    + "-" * 50
                )

            print(f"\nTotal de pacientes: {len(pacientes)}")

    # ============================
    # OPCIÓN 3: SALIR
    # ============================
    elif opcion == "3":
        print("\n¡Gracias por usar el CRM!\nCerrando sistema...")
        break

    else:
        print("\n✗ Opción no válida. Por favor selecciona 1, 2 o 3.")

print("\nSistema cerrado.")