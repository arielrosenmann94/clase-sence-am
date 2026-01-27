
valor_hallulla_un = 300
valor_marraquetas_un = 320

def sumar(a, b):
    sumar = a + b
    dinero_retiro = (a * valor_hallulla_un) + (b  * valor_marraquetas_un)


    return f"Hola hoy tienes que comprar {a} hallullas y {b} marraquetas y en total tienes que comprar{sumar} panes", f"Para la compra tienes qeu retirar ${dinero_retiro}"

print(sumar(9,3))


def restar(a, b):
    dinero_total = 100000
    caja = dinero_total- ((a * valor_hallulla_un) + (b  * valor_marraquetas_un))
    return caja
 
total_caja_chica = restar(9,3) # alamcena el retorno de la función en este caso es: 96340

print(total_caja_chica)


def saludar_usuario(nombre):
    print(f"hola buenos días {nombre}")

saludar_usuario(input("ingresa tu nombre: "))




def normalizar(texto):
    return texto.strip().lower()


def valor_compra(tipo, kg):
    #         Hallulla, 5
    
    tipo = normalizar(tipo)
#    Hallulla = hallulla
    print(tipo)
    valor_marrqueta = 2000
    valor_hallulla = 1600
    valor_amasado = 2400


    if tipo == "marraqueta":
    #hallulla   
        return valor_marrqueta * kg
    elif tipo == "hallulla":
    # hallulla
        return valor_hallulla * kg 
                            #   5
    
    elif tipo == "amasado":
        return valor_amasado * kg
    else: 
        return None
    
valor_compra("          Hallulla", 5)
