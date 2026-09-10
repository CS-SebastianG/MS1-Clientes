import mysql.connector
from mysql.connector import pooling
import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", 3307)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "rootpassword"),
    "database": os.getenv("DB_NAME", "restaurante_db"),
}

# Pool de conexiones (mejor rendimiento)
try:
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="ms1_pool",
        pool_size=5,
        pool_reset_session=True,
        **DB_CONFIG
    )
    print("Pool de conexiones MySQL creado correctamente")
except mysql.connector.Error as e:
    print(f"Error al crear el pool: {e}")
    connection_pool = None


def get_connection():
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