from datetime import datetime
from db import conectar
import bcrypt  # type: ignore

# Función para insertar un nuevo usuario
def insertar_usuario(nombres, apellidos, nombre_usuario, email, contraseña, cedula, año_seccion, fecha_registro, rol='usuario'):
    if usuario_existe(nombre_usuario, email, cedula):
        raise Exception("El usuario, correo electrónico o cédula ya están registrados.")

    hashed_password = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

    conn = conectar()
    cursor = conn.cursor()

    # Registrar usuario con año_seccion, fecha_registro y rol
    query = """
    INSERT INTO usuarios (nombres, apellidos, nombre_usuario, email, contraseña, cedula, año_seccion, fecha_registro, rol)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (nombres, apellidos, nombre_usuario, email, hashed_password, cedula, año_seccion, fecha_registro, rol))

    conn.commit()
    cursor.close()
    conn.close()

# Función para verificar si el usuario, correo o cédula ya existen
def usuario_existe(nombre_usuario, email, cedula):
    conn = conectar()
    cursor = conn.cursor()
    query = "SELECT id FROM usuarios WHERE nombre_usuario = %s OR email = %s OR cedula = %s"
    cursor.execute(query, (nombre_usuario, email, cedula))
    resultado = cursor.fetchone()

    cursor.fetchall()  # Consumir resultados pendientes para evitar errores de cursor
    cursor.close()
    conn.close()

    return resultado is not None

# Función para verificar credenciales de login y obtener el rol
def verificar_credenciales(usuario, contraseña):
    conn = conectar()
    cursor = conn.cursor()

    query = "SELECT contraseña, rol FROM usuarios WHERE nombre_usuario=%s OR email=%s"
    cursor.execute(query, (usuario, usuario))
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado:
        hashed_password = resultado[0].encode('utf-8')
        if bcrypt.checkpw(contraseña.encode('utf-8'), hashed_password):
            return True, resultado[1]
        else:
            return False, None
    return False, None

# Función para obtener el rol del usuario
def obtener_rol_usuario(usuario):
    conn = conectar()
    cursor = conn.cursor()
    
    query = "SELECT rol FROM usuarios WHERE nombre_usuario=%s OR email=%s"
    cursor.execute(query, (usuario, usuario))
    resultado = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return resultado[0] if resultado else None

# Función para obtener todos los datos del usuario
def obtener_datos_usuario(usuario):
    conn = conectar()
    cursor = conn.cursor()
    
    query = "SELECT nombres, apellidos, nombre_usuario, email, cedula, año_seccion, fecha_registro, rol FROM usuarios WHERE nombre_usuario=%s OR email=%s"
    cursor.execute(query, (usuario, usuario))
    resultado = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return resultado if resultado else None