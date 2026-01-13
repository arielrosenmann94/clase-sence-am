#lala

"""clave_correcta = 1234
intentos = 0
max_intentos = 3

print("Bienvenido al Cajero Automático")

while intentos < max_intentos:
    
    clave = int(input("Ingrese su contraseña de 4 dígitos: "))

    if clave == clave_correcta:
        print("Ingreso exitoso")
        break
    else:
        intentos += 1
        print("Contraseña incorrecta")
        print("Intento", intentos, "de", max_intentos)

        if intentos == max_intentos:
            print("Usuario bloqueado")"""


#Bastian

"""clave_correcta = "1234"
intentos = 3

while intentos > 0:
    clave = input("Ingrese la clave de su cuenta: ")
    if clave == clave_correcta:
        print("Acceso concedido")
        break
    else:
        intentos += 1
        print("Clave incorrecta.")
        print("Intento", intentos, "de", intentos)

        if intentos == 0:
            print("Has alcanzado el número máximo de intentos. Operación bloqueada.")

"""
#Rubi

'''# Variables iniciales
clave_correcta = "1234"
intentos = 0

print("--- BIENVENIDO AL BANCO ---")

while intentos < 3:
    # Pedimos la clave (la guardamos como texto para que los ceros a la izquierda no den problemas)
    clave_ingresada = int(input("Ingrese su clave de 4 dígitos: "))

    # 1. NEGACIÓN: ¿La clave es distinta a la correcta?
    if clave_ingresada != clave_correcta:
        intentos = intentos + 1
        print("Clave incorrecta.")
        
        # Si aún no llega al límite, le avisamos cuánto le queda
        if intentos < 3:
            print("Le quedan", 3 - intentos, "intentos.")
            print(f"Le quedan {3 - intentos} intentos")
        else:
            print("USUARIO BLOQUEADO. Comuníquese con el banco.")
            
    # 2. ÉXITO: Si no fue incorrecta, entonces es la correcta
    else:
        print("¡INGRESO EXITOSO!")
        break '''


#Nicolás

contraseña = "8942"
intentos = 3

while intentos > 0:
    ingreso = input("Por favor ingrese su contraseña \n")
    if ingreso != contraseña:
        intentos -= 1
        print("Contraseña incorrecta. Intente otra vez")
        print(f"intentos restantes, {intentos} intentos")
    else:
        print("Contraseña correcta. Ingreso autorizado")
        break
if intentos == 0:
    print("Contraseña incorrecta. Acceso bloqueado.")


#Octavio
intentos = 3
max_intentos = 0
contraseña_real = 1234

while intentos > max_intentos:
    contraseña = int(input("Ingrese Contraseña: "))

    if contraseña == contraseña_real:
        print("Contraseña aceptada")
        break
    else:
        intentos = intentos - 1
        print("Contraseña incorrecta. Intente nuevamente")
        print("Intentos restantess: ", intentos - max_intentos)

if intentos == max_intentos:
    print("Ha superado el número máximo de intentos")
    print("Operación Cancelada")


#Roberto

card_database = "X"
pin_database = 1234

card_input = input("Ingrese su tarjeta: ")

MAX_TRY = 3
count_try = 1

while count_try <= MAX_TRY:
    pin_input = int(input("Ingrese su clave: "))

    if card_input == card_database and pin_input == pin_database:
        print("Bienvenido")
        break
    else:
        count_try += 1
        if count_try > MAX_TRY:
            print("Ha superado el máximo de intentos. Acceso denegado.")
        else:
            print("La clave ingresada es incorrecta.")


#sergio
# Contraseña correcta del sistema
contraseña_correcta = "1234"

# Contador de intentos
intentos = 0
intentos_maximos = 3

# Variable para saber si ingresó correctamente
ingreso_exitoso = False

# Ciclo para los 3 intentos
while intentos < intentos_maximos:
    # Solicitar contraseña al usuario
    contraseña_ingresada = input("Ingrese su contraseña de 4 dígitos: ")
    
    # Limpiar espacios en blanco
    contraseña_ingresada = contraseña_ingresada.strip()
    
    # Incrementar el contador de intentos
    intentos = intentos + 1
    
    # Verificar si la contraseña es correcta
    if contraseña_ingresada == contraseña_correcta:
        print("Ingreso exitoso")
        ingreso_exitoso = True
        break
    else:
        # Calcular intentos restantes
        intentos_restantes = intentos_maximos - intentos
        
        if intentos_restantes > 0:
            print("Contraseña incorrecta. Le quedan", intentos_restantes, "intentos")
        else:
            print("Usuario bloqueado")