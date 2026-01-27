'''def saludar(parametro):
    print("cuerpo de la función")
    return #aca colocamos el retorno

saludar() #esta es la llamada



saludar = lambda parametro: print("el cuerpo de la función")'''

multiplicar = lambda x: x * 2

print(multiplicar(4))
#lo de arriba y lo de abajo funcionan igual
def multiplicar(x):
    resultado = x * 2
    return resultado

print(multiplicar(3))

#-------------------------------------------------------------


pagos = [
    {"cliente": "Platón", "atrasado": True},
    {"cliente": "Aristoteles", "atrasado": False},
    {"cliente": "Niche", "atrasado": True}
]

estado = bool(input("Que quieres filtrar?: (atrasados True or False)"))
atrasados = list(filter(lambda parametro: parametro["atrasado"] == estado, pagos))
print(atrasados)

cliente = input("Selecciona el nombre del cliente: ")
busacr_cliente = list(filter(lambda parametro: parametro["cliente"] == cliente, pagos))

print(busacr_cliente)