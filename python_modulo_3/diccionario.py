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

personas = {
    "nombre": "Juan", 
    "apellido": "Perez",
    "rut": "8547000-6"
}

personas = [
    {"id": 1,
     "nombre": "Juan", 
    "apellido": "Perez",
    "rut": "8547000-6"  },

    { "id": 2,
     "nombre": "Juan", 
    "apellido": "Perez",
    "rut": "8547000-6"},

    {"id": 3,
    "nombre": "Juan", 
    "apellido": "Perez",
    "rut": "8547000-6"
    }
]

diccionaro_personas = {
    1: {"nombre": "Juan", 
    "apellido": "Perez",
    "rut": "8547000-6"  },

    2: {
     "nombre": "Juan", 
    "apellido": "Perez",
    "rut": "8547000-6"},

    3: {"nombre": "Juan", 
    "apellido": "Perez",
    "rut": "8547000-6"
    }
}


print(diccionaro_personas)
print(diccionaro_personas[3])
print(diccionaro_personas[3]["nombre"])

cliente_premium = diccionaro_personas[3]["nombre"]

print(cliente_premium)

clientes = [
    {"id": 1, "rut":"8222333-6", "nombre": "maria rojas"},
    {"id": 2, "rut":"8222333-7", "nombre": "Marcos rojas"}
]

deudas = [
    {"id": 1, "id_cliente": 2, "monto_deuda": 55000 }
]

