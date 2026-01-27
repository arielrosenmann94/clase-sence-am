def normalizar(texto):
    return texto.strip().lower()


def valor_compra(tipo, kg):  
    tipo = normalizar(tipo)
    valor_marrqueta = 2000
    valor_hallulla = 1600
    valor_amasado = 2400


    if tipo == "marraqueta": 
        return valor_marrqueta * kg
    elif tipo == "hallulla":
        return valor_hallulla * kg 
    elif tipo == "amasado":
        return valor_amasado * kg
    else: 
        return None
    
#valor_compra(input("Qué pan llevas (hallulla / marraqueta / amasado)? "),input("Cuánto pesa?"))






