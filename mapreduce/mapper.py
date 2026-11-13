#!/usr/bin/env python3
import sys
from datetime import datetime

DIAS = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
cache = {}

for linea in sys.stdin:
    campos = linea.rstrip("\n").split(",")
    if len(campos) != 8 or campos[0] == "id":
        continue
    try:
        fecha = campos[1][:10]
        dia = cache.get(fecha)
        if dia is None:
            dia = DIAS[datetime.strptime(fecha, "%Y-%m-%d").weekday()]
            cache[fecha] = dia
        cantidad = int(campos[5])
        metodo = campos[7].strip()
        if not metodo:
            continue
    except (ValueError, IndexError):
        continue
    print(f"{metodo},{dia}\t{cantidad}")
