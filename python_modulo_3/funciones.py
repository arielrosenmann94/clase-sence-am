'''def nombre_funcion(parametro):
    print("el cuerpo de la función")
    return print("el retorno de la funcion")

# nombre_funcion(1)  #esto es la llamada a la función

def saludar():
    print("hola")


def saludamos(nombre):
    print(f"hola {nombre} te deseo un buen día")
    print("hola ", nombre, "te deseo un buen día")


saludamos("Entregar un parametro")


def sumar(a, b):
    print(a)
    print(b)
    suma = a + b
    return suma


edad_papa = 80

edad_mama = 90

edad_familiar = sumar(edad_mama, edad_papa)

print(edad_familiar)'''
valor_leche = 1400
valor_avena = 2400
valor_agua = 800

def mostrar_valor(item):
    if item == "leche":
        print(valor_leche)
    elif item == "avena":
        print(valor_avena)
    elif item == "agua":
        print(valor_agua)
    else:
        print("producto no existe llamar a supervisor")

codigo_barra = input("lector de codigo")

mostrar_valor(codigo_barra)

def cobrar(item):   
    if item == "leche":
        print("debes pagar: ", valor_leche)
    elif item == "avena":
        print("debes pagar: ", valor_avena)
    elif item == "agua":
        print("debes pagar: ", valor_agua)
    else:
        print("producto no existe llamar a supervisor")


cobrar(codigo_barra)