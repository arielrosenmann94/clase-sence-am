diccionario = {
    "clave": "un valor",
    "otra clave": 85,
    "una clave más": True
}

cliente = {
    "nombre": "Apolo",
    "edad": 5000,
    "ubicación": "Olimpo"
}

print("Este es el diccionario 'persona' completo: ", cliente)
print(type(cliente))

nombre_cliente = cliente["nombre"]
print("Este es el nombre del cliente: ", nombre_cliente)

cliente["edad"] = 10000
print("Datos actualizados del cliente: ", cliente)

cliente["correo"] = "soyapolo@olimpo.com"
print(cliente)




