#Roberto
# Configuración
MAX_TRY = 3
# Base de datos simulada de usuarios
users_database = [
    {
        "correo": "juan@mail.com",
        "username": "juan123",
        "password": "abc123"
    },
    {
        "correo": "maria@mail.com",
        "username": "maria89",
        "password": "pass456"
    },
    {
        "correo": "pedro@mail.com",
        "username": "pedro_dev",
        "password": "qwerty"
    }
]
# Registro de intentos por IP
ip_attempts = {}
# Simulación de IP
ip = input("Registrar IP: ")
# Inicializar contador si la IP no existe
if ip not in ip_attempts:
    ip_attempts[ip] = 0
# Verificar si la IP está bloqueada
if ip_attempts[ip] >= MAX_TRY:
    print("IP bloqueada por múltiples intentos fallidos.")
else:
    while ip_attempts[ip] < MAX_TRY:
        user_input = input("Ingrese su correo o username: ")
        password_input = input("Ingrese su contraseña: ")
        acceso_permitido = False
        for user in users_database:
            if (
                (user_input == user["correo"] or user_input == user["username"])
                and password_input == user["password"]
            ):
                acceso_permitido = True
                break
        if acceso_permitido:
            print("Acceso permitido. Bienvenido.")
            break
        else:
            ip_attempts[ip] += 1
            if ip_attempts[ip] >= MAX_TRY:
                print("Acceso denegado. IP bloqueada.")
            else:
                print("Usuario o contraseña incorrectos. Intente nuevamente.")
#Bastián
# Diccionario con 3 usuarios
usuarios = {
    "juan": "1234",
    "maria": "abcd",
    "pedro": "pass123"
}
intentos = 0
while intentos < 3:
    usuario = input("Ingrese usuario: ")
    password = input("Ingrese contraseña: ")
    if usuario in usuarios and usuarios[usuario] == password:
        print("Acceso permitido")
        break
    else:
        print("Usuario o contraseña incorrectos")
        intentos = intentos + 1
        print("Intentos fallidos:", intentos)
if intentos == 3:
    print("Acceso bloqueado por demasiados intentos fallidos")

#sergio
# Base de datos de usuarios (diccionario con usuarios)
usuarios = {
    "juan@email.com": {
        "username": "juan123",
        "password": "pass123",
        "nombre": "Juan Pérez"
    },
    "maria@email.com": {
        "username": "maria456",
        "password": "pass456",
        "nombre": "María González"
    },
    "carlos@email.com": {
        "username": "carlos789",
        "password": "pass789",
        "nombre": "Carlos Rodríguez"
    }
}



#https://claude.ai/share/92cdf9de-e3d3-4186-9d60-6cb10b2989bf lectura del código de abajo
# Lista para almacenar IPs bloqueadas (simulación)
ips_bloqueadas = []
intentos_fallidos = {}

# Simulación de IP del usuario
ip_usuario = "192.168.1.100"

# Función para verificar si la IP está bloqueada
def ip_bloqueada(ip):
    return ip in ips_bloqueadas

# Función para buscar usuario por correo o username
def buscar_usuario(identificador, password):
    # Buscar por correo (clave del diccionario)
    if identificador in usuarios:
        if usuarios[identificador]["password"] == password:
            return usuarios[identificador]
    
    # Buscar por username
    for correo, datos in usuarios.items():
        if datos["username"] == identificador and datos["password"] == password:
            return datos
    
    return None

# Sistema de inicio de sesión
print("=== SISTEMA DE INICIO DE SESIÓN ===\n")

# Verificar si la IP está bloqueada
if ip_bloqueada(ip_usuario):
    print(f"❌ ACCESO DENEGADO: Tu IP ({ip_usuario}) ha sido bloqueada por múltiples intentos fallidos.")
else:
    # Inicializar contador de intentos para esta IP
    if ip_usuario not in intentos_fallidos:
        intentos_fallidos[ip_usuario] = 0
    
    # Permitir hasta 3 intentos
    while intentos_fallidos[ip_usuario] < 3:
        print(f"\nIntentos restantes: {3 - intentos_fallidos[ip_usuario]}")
        
        # Solicitar credenciales
        identificador = input("Ingresa tu correo o username: ")
        password = input("Ingresa tu contraseña: ")
        
        # Verificar credenciales
        usuario = buscar_usuario(identificador, password)
        
        if usuario:
            print(f"\n✅ ACCESO PERMITIDO")
            print(f"Bienvenido/a {usuario['nombre']}!")
            # Reiniciar intentos fallidos al iniciar sesión exitosamente
            intentos_fallidos[ip_usuario] = 0
            break
        else:
            intentos_fallidos[ip_usuario] += 1
            print(f"\n❌ ACCESO DENEGADO: Usuario o contraseña incorrectos.")
            
            # Verificar si se alcanzó el límite de intentos
            if intentos_fallidos[ip_usuario] >= 3:
                ips_bloqueadas.append(ip_usuario)
                print(f"\n🚫 IP BLOQUEADA: Has excedido el número de intentos permitidos.")
                print(f"La IP {ip_usuario} ha sido bloqueada.")
                break

print("\n=== FIN DEL PROGRAMA ===")