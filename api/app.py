import os
import time

import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, request

app = Flask(__name__)

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "db"),
    "port": os.environ.get("DB_PORT", "5432"),
    "dbname": os.environ["POSTGRES_DB"],
    "user": os.environ["POSTGRES_USER"],
    "password": os.environ["POSTGRES_PASSWORD"],
}

CREAR_TABLA = """
CREATE TABLE IF NOT EXISTS resultados (
    id SERIAL PRIMARY KEY,
    metodo_pago TEXT NOT NULL,
    dia_semana TEXT NOT NULL,
    unidades BIGINT NOT NULL,
    UNIQUE (metodo_pago, dia_semana)
)
"""


def conectar():
    ultimo_error = None
    for _ in range(15):
        try:
            return psycopg2.connect(**DB_CONFIG)
        except psycopg2.OperationalError as e:
            ultimo_error = e
            time.sleep(2)
    raise ultimo_error


def consulta(sql, params=(), fetch=True):
    conn = conectar()
    try:
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(sql, params)
                filas = cur.fetchall() if fetch else None
                return filas, cur.rowcount
    finally:
        conn.close()


@app.get("/resultados")
def listar():
    filas, _ = consulta("SELECT * FROM resultados ORDER BY metodo_pago, id")
    return jsonify(filas)


@app.get("/resultados/<metodo>")
def por_metodo(metodo):
    filas, _ = consulta(
        "SELECT * FROM resultados WHERE LOWER(metodo_pago) = LOWER(%s) ORDER BY id",
        (metodo,),
    )
    if not filas:
        return jsonify({"error": "metodo de pago no encontrado"}), 404
    return jsonify(filas)


@app.post("/resultados")
def crear():
    datos = request.get_json(silent=True) or {}
    try:
        metodo = datos["metodo_pago"]
        dia = datos["dia_semana"]
        unidades = int(datos["unidades"])
    except (KeyError, ValueError):
        return jsonify({"error": "se requieren metodo_pago, dia_semana y unidades"}), 400
    filas, _ = consulta(
        "INSERT INTO resultados (metodo_pago, dia_semana, unidades) VALUES (%s, %s, %s) "
        "ON CONFLICT (metodo_pago, dia_semana) DO UPDATE SET unidades = EXCLUDED.unidades "
        "RETURNING *",
        (metodo, dia, unidades),
    )
    return jsonify(filas[0]), 201


@app.put("/resultados/<metodo>/<dia>")
def actualizar(metodo, dia):
    datos = request.get_json(silent=True) or {}
    try:
        unidades = int(datos["unidades"])
    except (KeyError, ValueError):
        return jsonify({"error": "se requiere unidades"}), 400
    filas, _ = consulta(
        "UPDATE resultados SET unidades = %s WHERE metodo_pago = %s AND dia_semana = %s RETURNING *",
        (unidades, metodo, dia),
    )
    if not filas:
        return jsonify({"error": "registro no encontrado"}), 404
    return jsonify(filas[0])


@app.delete("/resultados/<metodo>/<dia>")
def borrar(metodo, dia):
    _, n = consulta(
        "DELETE FROM resultados WHERE metodo_pago = %s AND dia_semana = %s",
        (metodo, dia),
        fetch=False,
    )
    if n == 0:
        return jsonify({"error": "registro no encontrado"}), 404
    return jsonify({"eliminados": n})


if __name__ == "__main__":
    consulta(CREAR_TABLA, fetch=False)
    app.run(host="0.0.0.0", port=5000)
