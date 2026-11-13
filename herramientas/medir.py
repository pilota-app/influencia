#!/usr/bin/env python3
"""Vuelve a medir los eventos de cripto con las velas diarias públicas de Binance. Solo biblioteca estándar.

Para cada evento con activo cripto (BTC, ETH, BNB, DOGE…): el cambio del día (cierre del día anterior → cierre del día
del evento) y a 1, 5, 20 y 60 días. Así cualquiera puede revisar los números. Las acciones se midieron con Yahoo Finance
(cierre ajustado) y aquí no se tocan.

  python3 herramientas/medir.py            → muestra las diferencias
  python3 herramientas/medir.py --guardar  → las escribe en eventos.json
"""
import datetime
import json
import os
import sys
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.binance.com/api/v3/klines"
DIA_MS = 86_400_000
CRIPTO = {"BTC", "ETH", "BNB", "DOGE", "SOL", "XRP", "ADA", "TRX"}


def velas(simbolo, desde_ms, cuantas=70):
    url = f"{API}?symbol={simbolo}USDT&interval=1d&startTime={desde_ms}&limit={cuantas}"
    with urllib.request.urlopen(url, timeout=20) as r:
        return [(int(v[0]), float(v[4])) for v in json.load(r)]


def medir(e):
    dia = int(datetime.datetime.fromisoformat(e["fecha"]).replace(tzinfo=datetime.timezone.utc).timestamp() * 1000)
    v = velas(e["activo"], dia - DIA_MS)
    if len(v) < 2 or v[1][0] != dia:
        return None
    base = v[0][1]
    salida = {"dia": round(v[1][1] / base - 1, 3)}
    for h in (1, 5, 20, 60):
        salida[f"d{h}"] = round(v[1 + h][1] / base - 1, 3) if 1 + h < len(v) else None
    return salida


if __name__ == "__main__":
    ruta = os.path.join(RAIZ, "eventos.json")
    eventos = json.load(open(ruta, encoding="utf-8"))
    for e in eventos:
        if e["activo"] not in CRIPTO:
            continue
        nuevo = medir(e)
        if nuevo and nuevo != e["movimiento"]:
            print(e["id"], e["fecha"], e["activo"], e["movimiento"], "→", nuevo)
            e["movimiento"] = nuevo
            d, d20 = nuevo["dia"], nuevo["d20"]
            e["duro_20d"] = None if d20 is None else (d20 * d > 0 and abs(d20) >= abs(d) / 2)
    if "--guardar" in sys.argv:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(eventos, f, indent=1, ensure_ascii=False)
