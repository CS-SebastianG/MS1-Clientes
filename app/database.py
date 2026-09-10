import mysql.connector
from mysql.connector import pooling
import os
import time

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", 3307)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "rootpassword"),
    "database": os.getenv("DB_NAME", "restaurante_db"),
}


def _crear_pool(intentos=10, espera_seg=3):
    """Intenta crear el pool con reintentos, por si MySQL aun no acepta
    conexiones apenas arranca el contenedor (aunque el healthcheck ya haya
    pasado). Evita que un fallo puntual de timing deje connection_pool en
    None para siempre."""
    for intento in range(1, intentos + 1):
        try:
            pool = pooling.MySQLConnectionPool(
                pool_name="ms1_pool",
                pool_size=5,
                pool_reset_session=True,
                **DB_CONFIG
            )
            print("Pool de conexiones MySQL creado correctamente")
            return pool
        except mysql.connector.Error as e:
            print(f"Intento {intento}/{intentos}: error al crear el pool: {e}")
            if intento < intentos:
                time.sleep(espera_seg)
    print("No se pudo crear el pool de conexiones tras varios intentos")
    return None


connection_pool = _crear_pool()


def get_connection():
    global connection_pool
    if connection_pool is None:
        # Ultimo intento bajo demanda, por si MySQL tardo mas de lo esperado
        connection_pool = _crear_pool(intentos=1)
        if connection_pool is None:
            raise Exception("Pool de conexiones no disponible")
    return connection_pool.get_connection()


def test_connection():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM clientes")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return f"Conexión Ok :) . Clientes en BD: {count}"
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    print(test_connection())
