##Lala
#
#intentos = 0
#max_intentos = 3
#
#print("Bienvenido al Cajero Automático")
#print("Este cajero solo entrega billetes de $10.000")
#
#while intentos < max_intentos:
#    monto = int(input("Ingrese el monto que desea retirar: "))
#
#    if monto % 10000 == 0:
#        print("Monto correcto.")
#        print("Retire su dinero:", monto)
#        break
#    else:
#        intentos += 1
#        print("Monto incorrecto.")
#        print("Intento", intentos, "de", max_intentos)
#
#        if intentos == max_intentos:
#            print("Ha superado el máximo de intentos. Operación cancelada.")
#
#
## rubi
#intentos = 0
#
#print("Bienvenido al cajero. Solo tenemos billetes de $10.000")
#
## Mientras no hayamos fallado 3 veces, el programa sigue
#while intentos < 3:
#    # Pedimos el número al usuario
#    monto = int(input("Ingrese el monto a retirar: "))
#
#    # Verificamos si es múltiplo de 10.000
#    if monto % 10000 == 0:
#        print("Monto correcto. Retire su dinero.")
#        intentos = 10  # Cambiamos intentos a 10 para que la condición del 'while' deje de cumplirse
#    else:
#        intentos = intentos + 1
#        print("Monto incorrecto.")
#        
#        # Si todavía le quedan chances, le decimos cuántas
#        if intentos < 3:
#            print("Le quedan", 3 - intentos, "oportunidades.")
#        else:
#            print("Ha superado el límite de intentos.")
#
#
#Nicolás

#intentos = 3
#
#while intentos > 0:
#    monto= int(input("Bienvenido, ¿Cuánto dinero desea retirar?"))
#    if monto % 5 != 0:
#        print("Monto incorrecto, por favor intente de nuevo con un valor múltiplo de 5")
#        intentos = intentos - 1
#    else:
#        print("Transacción aprobada!")

#Sergio

'''print("=" * 50)
print("BIENVENIDO AL CAJERO AUTOMÁTICO")
print("=" * 50)
print("INFORMACIÓN: Solo disponemos de billetes de $10.000")
print()

# Variable para controlar los intentos
intentos = 0
max_intentos = 3
retiro_exitoso = False

# Ciclo while para dar hasta 3 intentos
while intentos < max_intentos:
    print(f"Intento {intentos + 1} de {max_intentos}")
    
    try:
        # Solicitar el monto al usuario
        monto = int(input("Ingrese el monto a retirar: $"))
        
        # Verificar que el monto sea positivo
        if monto <= 0:
            print("ERROR: El monto debe ser mayor a cero")
            print()
            intentos = intentos + 1
        # Verificar que el monto sea múltiplo de 10000
        elif monto % 10000 == 0:
            print()
            print("✓ RETIRO EXITOSO")
            print(f"Se han entregado ${monto}")
            billetes = monto // 10000
            print(f"Cantidad de billetes: {billetes} billetes de $10.000")
            print()
            print("Gracias por usar nuestro cajero automático")
            retiro_exitoso = True
            break  # Salir del ciclo si el retiro fue exitoso
        else:
            print()
            print("✗ MONTO INCORRECTO")
            print("El monto debe ser múltiplo de $10.000")
            print("Ejemplos válidos: $10.000, $20.000, $50.000, etc.")
            print()
            intentos = intentos + 1
    
    except:
        print("ERROR: Debe ingresar un número válido")
        print()
        intentos = intentos + 1

# Verificar si se agotaron los intentos
if intentos == max_intentos and retiro_exitoso == False:
    print()
    print("=" * 50)
    print("MÁXIMO DE INTENTOS ALCANZADO")
    print("Su tarjeta ha sido retenida por seguridad")
    print("Por favor, comuníquese con su banco")
    print("=" * 50)'''

#octavio
'''intentos = 0
max_intentos = 3

while intentos < max_intentos:
    monto = int(input("Ingrese el monto a retirar (solo billetes de $10.000): "))

    if monto > 0 and monto % 10000 == 0:
        billetes = monto // 10000
        print("Retiro exitoso.")
        print("Se entregan", billetes, "billetes de $10.000")
        break
    else:
        intentos = intentos + 1
        print("Monto inválido. Intente nuevamente.")
        print("Intentos restantes:", max_intentos - intentos)

if intentos == max_intentos:
    print("Ha superado el número máximo de intentos.")
    print("Operación cancelada.")'''


#Denissa

'''print("=" * 50)
print("BIENVENIDO AL CAJERO AUTOMÁTICO")
print("=" * 50)
print("INFORMACIÓN: Solo disponemos de billetes de $10.000")
print()

intentos = 0
max_intentos = 3
retiro_exitoso = False

while intentos < max_intentos:
    print(f"Intento {intentos + 1} de {max_intentos}")

    try:
        monto = int(input("Ingrese el monto a retirar: $"))

        if monto <= 0:
            print("ERROR: El monto debe ser mayor a cero\n")
            intentos += 1

        elif monto % 10000 == 0:
            billetes = monto // 10000
            print("\n✓ RETIRO EXITOSO")
            print(f"Se han entregado ${monto}")
            print(f"Cantidad de billetes: {billetes} billetes de $10.000\n")
            print("Gracias por usar nuestro cajero automático")
            retiro_exitoso = True
            break

        else:
            print("\n✗ MONTO INCORRECTO")
            print("El monto debe ser múltiplo de $10.000")
            print("Ejemplos válidos: $10.000, $20.000, $50.000, etc.\n")
            intentos += 1

    except ValueError:
        print("ERROR: Debe ingresar un número válido\n")
        intentos += 1

if intentos == max_intentos and not retiro_exitoso:
    print("\n" + "=" * 50)
    print("MÁXIMO DE INTENTOS ALCANZADO")
    print("Su tarjeta ha sido retenida por seguridad")
    print("Por favor, comuníquese con su banco")
    print("=" * 50)
'''

#Roberto

'''card_database = "X"

pin_database = "Y"

card_input = input("Ingrese su tarjeta: ")

pin_input = input("Ingrese su clave: ")

if (card_input != card_database) or (pin_input != pin_database):
    print("Acceso denegado")

else:
     cash_input = int(input("Este cajero solo tiene billetes de $10.000. Ingrese el monto: "))

MAX_TRY = 3

count_try = 1

while count_try <= MAX_TRY:
    if cash_input % 10000 != 0:
        print("El monto ingresado no es correcto. Ingrese monto: ")
        count_try += 1

    else:
        print("Retire su diero,")
    break
    '''

print("BIENVENIDO AL CAJERO AUTOMÁTICO")
print("=" * 50)
print("INFORMACIÓN: Solo disponemos de billetes de $10.000")
print()

while True:
    monto_ingresado = input("ingrese un monto de dinero a retirar: ").strip()
    print(monto_ingresado)

    try:
        monto = int(monto_ingresado)
    except ValueError:
        continue

    if monto == 0:
        print("operación cancelada")
        break

    if monto > 0 and monto % 10000 == 0:
        print(f"retiro aceptado, retire el monto de {monto}")
        break

    else:
        print("retiro rechazado, el monto debe ser múltiplo de 10000")


print("la app web se sigue ejecutando")