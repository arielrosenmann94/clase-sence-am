numero_entero = 45 #Esto es un int

print(numero_entero)
print(type(numero_entero))

numero_decimal = 8.5 #esto es un float

print("la variable numero_decimal contiene el valor: ", numero_decimal, "Es un tipo de dato: ", type(numero_decimal))

cadena_texto = "Esto es una cadena de texto" #Esto es un string (str)
Cadena_texto = "esto es otra cadena de texo"
Cadena_Texto = "esto es una tercera cadena de texto"

print(cadena_texto)
print(type(cadena_texto))

esto_es_verdadero = True
esto_es_falso = False

print(esto_es_verdadero)
print(esto_es_falso)
print(type(esto_es_falso))

x = None
print("el valor de x es", x)
print(type(x))
x = 5
print("el valor de x ahora es", x)
print("el tipo de dato de x ahora es",type(x))

y = ""
print("el valor de y es:", y)
print(type(y))

y = "5"
print('el valor de "y" ahora es:', y)
print("el tipo de dato de 'y' es:", type(y))

esto_es_tuple = ("Juan", 31, "santiago", 2026, 22.5, True)

print(esto_es_tuple)
print(type(esto_es_tuple))


esto_es_lista = ["Ariel", 31, "santiago", 2026, 22.5, True]

print(esto_es_lista)
print(type(esto_es_lista))

otra_lista = ["string", "cadenas de texto", 25, 25.6, True, False, ["esto es otra lista", "dentro de la lista", 34, True], 78, ("esto es una tupla", 24, True)  ]

print(otra_lista)
print(type(otra_lista))

print("")
l = [1 , 2 , 1, "Hola", True ]
t = (1, 2 , 1, "Hola", True)

# También esxisten los SET
s = {1, 1, 2, "hola", True} #El SET elimina los bool y los elementos duplicados
print(s)
print(type(s))

#abajo es un diccionario arriba un SET
d = {"clave": 1, "otra clave": "Otro valor"} 

rojo = 1
amarillo = 2
azul = 3 

colores = (rojo, amarillo, azul)
