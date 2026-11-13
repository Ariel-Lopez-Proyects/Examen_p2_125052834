#!/usr/bin/env python3
import sys
from collections import defaultdict
from datetime import datetime

DIAS = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
cache = {}
totales = defaultdict(int)

with open(sys.argv[1], encoding="utf-8") as f:
    for linea in f:
        campos = linea.rstrip("\n").split(",")
        if len(campos) != 8 or campos[0] == "id":
            continue
        try:
            fecha = campos[1][:10]
            dia = cache.get(fecha)
            if dia is None:
                dia = DIAS[datetime.strptime(fecha, "%Y-%m-%d").weekday()]
                cache[fecha] = dia
            totales[(campos[7].strip(), dia)] += int(campos[5])
        except (ValueError, IndexError):
            continue

for (metodo, dia) in sorted(totales):
    print(f"{metodo},{dia}\t{totales[(metodo, dia)]}")
