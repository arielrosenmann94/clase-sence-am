opcion_texto = input("Elige una opción (1. ver saldo / 2. retirar dinero / 3.cambiar clave): ")


if opcion_texto.isdigit():
    opcion = int(opcion_texto)

    if opcion == 1:
        print("tu saldo es $50.000")

    if opcion == 2:
        print("Este cajero no tiene dinero")
    
    if opcion == 3:
        print("Esta función no está disponible para ti, anda a una sucursal")
        
    else:
        print("la opción seleccionada es inválida")
    
else:
    print("Opción invalida, escribe un número")



# Acá abajo se escribe la misma función de arriba pero con un switch

opcion_texto = input("Elige una opción (1. ver saldo / 2. retirar dinero / 3.cambiar clave): ")


if opcion_texto.isdigit():
    opcion = int(opcion_texto)

    respuestas_switch = {
        1: "tu saldo es $50.000",
        2: "Este cajero no tiene dinero",
        3: "Esta función no está disponible para ti, anda a una sucursal"
    }

    print(respuestas_switch.get(opcion, "la opción seleccionada es inválida"))

else:
    print("Opción invalida, escribe un número")

'''
if opcion_texto != None:
    print("enviar al registro de log")'''


