from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from app.database import get_connection


app = FastAPI(
    title="MS1 - Clientes y Pedidos",
    description="Microservicio de gestión de clientes y pedidos del restaurante",
    version="1.0.0",
    contact={
        "name": "Equipo Cloud Computing",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
def root():
    return {
        "servicio": "MS1 - Clientes y Pedidos",
        "estado": "activo",
        "version": "1.0.0",
        "documentacion": "/docs",
    }


@app.get("/health", tags=["Root"])
def health():

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"DB error: {e}")



@app.get("/clientes", tags=["Clientes"])
def listar_clientes(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM clientes ORDER BY id LIMIT %s OFFSET %s",
        (limit, offset),
    )
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"total": len(result), "clientes": result}


@app.get("/clientes/{cliente_id}", tags=["Clientes"])
def obtener_cliente(cliente_id: int):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes WHERE id = %s", (cliente_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if not result:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return result


@app.get("/clientes/{cliente_id}/pedidos", tags=["Clientes"])
def pedidos_de_cliente(cliente_id: int):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM pedidos WHERE cliente_id = %s ORDER BY fecha_pedido DESC",
        (cliente_id,),
    )
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"cliente_id": cliente_id, "total_pedidos": len(result), "pedidos": result}


@app.get("/clientes/buscar/", tags=["Clientes"])
def buscar_clientes_por_email(email: str = Query(..., min_length=3)):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM clientes WHERE email LIKE %s",
        (f"%{email}%",),
    )
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"total": len(result), "clientes": result}



@app.get("/pedidos", tags=["Pedidos"])
def listar_pedidos(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT p.id, p.fecha_pedido, p.total, p.estado,
               c.id AS cliente_id, c.nombre AS cliente_nombre, c.email AS cliente_email
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.id
        ORDER BY p.fecha_pedido DESC
        LIMIT %s OFFSET %s
        """,
        (limit, offset),
    )
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"total": len(result), "pedidos": result}


@app.get("/pedidos/{pedido_id}", tags=["Pedidos"])
def obtener_pedido(pedido_id: int):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT p.*, c.nombre AS cliente_nombre, c.email AS cliente_email
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.id
        WHERE p.id = %s
        """,
        (pedido_id,),
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if not result:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return result


@app.get("/pedidos/estado/{estado}", tags=["Pedidos"])
def pedidos_por_estado(estado: str):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT p.id, p.fecha_pedido, p.total, p.estado,
               c.nombre AS cliente_nombre
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.id
        WHERE p.estado = %s
        ORDER BY p.fecha_pedido DESC
        """,
        (estado,),
    )
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"estado": estado, "total": len(result), "pedidos": result}




@app.get("/pedidos/estadisticas/por-estado", tags=["Analítica"])
def estadisticas_por_estado():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT estado,
               COUNT(*) AS cantidad,
               SUM(total) AS monto_total,
               AVG(total) AS promedio
        FROM pedidos
        GROUP BY estado
        ORDER BY cantidad DESC
        """
    )
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"estadisticas": result}


@app.get("/clientes/estadisticas/top", tags=["Analítica"])
def top_clientes(limit: int = Query(5, ge=1, le=20)):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT c.id, c.nombre, c.email,
               COUNT(p.id) AS total_pedidos,
               SUM(p.total) AS monto_total
        FROM clientes c
        JOIN pedidos p ON c.id = p.cliente_id
        GROUP BY c.id, c.nombre, c.email
        ORDER BY monto_total DESC
        LIMIT %s
        """,
        (limit,),
    )
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"top_clientes": result}