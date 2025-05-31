from db import conectar

try:
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM alimentos;")
    datos = cursor.fetchall()
    print("📦 Datos en alimentos:", datos)
    conexion.close()
except Exception as e:
    print(f"❌ Error en la consulta: {e}")