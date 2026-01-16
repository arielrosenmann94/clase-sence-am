a = 15
b = 8
c = 5

suma = a + b

print("el valor de la suma es:", suma)

resta = a - b

print("el valor de la resta es:", resta)

multiplicacion = a * b

print("el valor de la multiplicación", multiplicacion)

division = int(a / c)
print("la división, forzando el tipo de dato, es: ", division)

division = a / c
print("la división es: ", division)
print(type(division))

division = str(a / c)
print("la división esta siendofrozada a str, y ahora es de tipo: ", type(division))


modulo = a % b

print("el modulo de a sobre b es: ", modulo)

potencia = a ** b
print("la potencia es: ", potencia )