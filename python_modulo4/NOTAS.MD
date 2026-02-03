Cliente (class)
rut: int
dv: int
nombre: string
segundo nombre: string
primer_apellido: sitrng
segundo_apellido: string
email: string (Email)
Relación con psicologo los datos del psicologo no se guardan dentro de la tabla clientes y un cliente puede tener muhcos piscologos, pero solo uno activo



psicologos

nombre
rut: int
dv: int
nombre: string
segundo nombre: string
primer_apellido: sitrng
segundo_apellido: string
email: string (Email)
especialidad: TipoEspecialidad
Relacion con cliente ( lo datos del cliente no se guardan dentro del psicolo, un psicologo puede tener muchos clientes)

ENUM TipoEspecialidad: 
    Infantil
    Adulto
    









