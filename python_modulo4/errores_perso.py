class NombreNoneError(Exception):
    pass


nombre = None

if nombre is None:
    raise NombreNoneError("EL nombre no puede ser None")




print("el programa continua")