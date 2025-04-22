from datetime import datetime
from db_usuarios import conectar
import bcrypt # type: ignore

# Función para insertar un nuevo usuario
def insertar_usuario(nombres, apellidos, nombre_usuario, email, contraseña, rol='usuario'):
    # Verificar si el usuario o correo ya existen
    if usuario_existe(nombre_usuario, email):
        raise Exception("El usuario o correo electrónico ya está registrado.")

    # Encriptar contraseña
    hashed_password = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

    # Conexión a la base de datos
    conn = conectar()
    cursor = conn.cursor()

    # Registrar usuario con rol
    fecha_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = """
    INSERT INTO usuarios (nombres, apellidos, nombre_usuario, email, contraseña, fecha_registro, rol)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (nombres, apellidos, nombre_usuario, email, hashed_password, fecha_registro, rol))
    conn.commit()
    cursor.close()
    conn.close()

# Función para verificar si el usuario o correo ya existen
def usuario_existe(nombre_usuario, email):
    conn = conectar()
    cursor = conn.cursor()
    query = "SELECT * FROM usuarios WHERE nombre_usuario = %s OR email = %s"
    cursor.execute(query, (nombre_usuario, email))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado is not None

# Función para verificar las credenciales de login y obtener el rol
def verificar_credenciales(usuario, contraseña):
    conn = conectar()
    cursor = conn.cursor()

    # Buscar el hash de la contraseña y el rol desde la base de datos
    query = "SELECT contraseña, rol FROM usuarios WHERE nombre_usuario=%s OR email=%s"
    cursor.execute(query, (usuario, usuario))  # Buscamos por nombre_usuario o email
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

# Función para obtener el rol de un usuario (opcional)
def obtener_rol_usuario(usuario):
    conn = conectar()
    cursor = conn.cursor()
    query = "SELECT rol FROM usuarios WHERE nombre_usuario=%s OR email=%s"
    cursor.execute(query, (usuario, usuario))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    if resultado:
        return resultado[0]
    return None