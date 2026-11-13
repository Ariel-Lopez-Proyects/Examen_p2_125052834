import os
import sys

import psycopg2

RUTA = sys.argv[1] if len(sys.argv) > 1 else "/data/output/resultado/part-00000"

conn = psycopg2.connect(
    host=os.environ.get("DB_HOST", "db"),
    port=os.environ.get("DB_PORT", "5432"),
    dbname=os.environ["POSTGRES_DB"],
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
)

cargados = 0
with conn, conn.cursor() as cur:
    cur.execute(
        "CREATE TABLE IF NOT EXISTS resultados ("
        "id SERIAL PRIMARY KEY, metodo_pago TEXT NOT NULL, dia_semana TEXT NOT NULL, "
        "unidades BIGINT NOT NULL, UNIQUE (metodo_pago, dia_semana))"
    )
    with open(RUTA, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            clave, valor = linea.split("\t")
            metodo, dia = clave.split(",")
            cur.execute(
                "INSERT INTO resultados (metodo_pago, dia_semana, unidades) VALUES (%s, %s, %s) "
                "ON CONFLICT (metodo_pago, dia_semana) DO UPDATE SET unidades = EXCLUDED.unidades",
                (metodo, dia, int(valor)),
            )
            cargados += 1

conn.close()
print(f"Registros cargados: {cargados}")
