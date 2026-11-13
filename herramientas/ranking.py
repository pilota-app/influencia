#!/usr/bin/env python3
"""Arma ranking.json desde personas.json y eventos.json. Solo biblioteca estándar.

El puntaje de una persona sale de sus eventos medidos, no de una opinión:
  peso de un evento = 0,5 ^ (años desde el evento)     (la influencia se gasta: a un año pesa la mitad)
  puntaje = movimiento medio del día con esos pesos (en valor absoluto, en %) × confianza
  confianza = min(1, suma de pesos / 3)                (pocos eventos o muy viejos achican el puntaje)
Una persona sin eventos queda en el ranking como «sin medir», al final.
"""
import datetime
import json
import os
import statistics

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PESO_PARA_CONFIAR = 3
VIDA_MEDIA_AÑOS = 1.0


def armar(personas, eventos, hoy=None):
    hoy = hoy or datetime.date.today()
    filas = []
    for p in personas:
        suyos = [e for e in eventos if e.get("persona") == p["id"] and e["movimiento"].get("dia") is not None]
        if not suyos:
            filas.append({"id": p["id"], "nombre": p["nombre"], "eventos": 0, "puntaje": None, "estado": "sin_medir"})
            continue
        dia = [abs(e["movimiento"]["dia"]) for e in suyos]
        duro = [e["duro_20d"] for e in suyos if e.get("duro_20d") is not None]
        pesos = [0.5 ** ((hoy - datetime.date.fromisoformat(e["fecha"])).days / 365 / VIDA_MEDIA_AÑOS) for e in suyos]
        medio = sum(w * x for w, x in zip(pesos, dia)) / sum(pesos)
        confianza = min(1.0, sum(pesos) / PESO_PARA_CONFIAR)
        filas.append({"id": p["id"], "nombre": p["nombre"], "eventos": len(suyos),
                      "movimiento_medio_dia": round(statistics.mean(dia), 4),
                      "movimiento_reciente_dia": round(medio, 4), "peso_reciente": round(sum(pesos), 2),
                      "duro_20d": round(sum(duro) / len(duro), 3) if duro else None,
                      "ultimo_evento": max(e["fecha"] for e in suyos),
                      "puntaje": round(medio * confianza * 100, 2), "estado": "medido"})
    filas.sort(key=lambda f: (f["puntaje"] is None, -(f["puntaje"] or 0)))
    for i, f in enumerate(filas):
        f["puesto"] = i + 1
    return filas


if __name__ == "__main__":
    personas = json.load(open(os.path.join(RAIZ, "personas.json"), encoding="utf-8"))
    eventos = json.load(open(os.path.join(RAIZ, "eventos.json"), encoding="utf-8"))
    ranking = armar(personas, eventos)
    with open(os.path.join(RAIZ, "ranking.json"), "w", encoding="utf-8") as f:
        json.dump({"formato": 1, "personas": len(personas), "eventos": len(eventos), "ranking": ranking}, f,
                  indent=1, ensure_ascii=False)
    for r in ranking:
        print(r["puesto"], r["nombre"], r["estado"], r.get("puntaje"))
