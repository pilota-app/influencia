# Influencia

Las personas que mueven el precio de las criptos y de las acciones de EE. UU., con cada evento fechado y medido.
Pilota lo puede leer para su análisis. Son datos abiertos: cualquiera puede revisar cada número.

**Estado: borrador (noviembre de 2026).** Tiene 18 personas y 27 eventos. Solo 3 personas tienen eventos medidos.
La meta es llegar a 500 personas, pero una persona entra al ranking con puntaje solo cuando tiene eventos medidos.

## Qué hay

| Archivo | Qué tiene |
|---|---|
| `personas.json` | Quién es cada persona, su rol, en qué mercados influye, qué activos mueve y sus cuentas públicas. `rol_verificado` dice si el rol se revisó con una fuente (`fuente_rol`) y en qué fecha. |
| `eventos.json` | Cada evento: quién, la fecha (el primer día con precio después de la noticia), qué pasó, el activo, la fuente y cuánto se movió el precio ese día y 1, 5, 20 y 60 días después. `duro_20d` dice si el efecto seguía 20 días después. |
| `ranking.json` | El ranking calculado. Lo genera `herramientas/ranking.py`. No se edita a mano. |
| `herramientas/medir.py` | Vuelve a medir los eventos de cripto con las velas públicas de Binance. |
| `herramientas/ranking.py` | Calcula el puntaje y el puesto de cada persona. |

## Cómo se calcula el puntaje

1. Cada evento tiene una fecha y una fuente. Sin fuente, el evento no cuenta.
2. El movimiento es el cambio del precio de cierre del día del evento contra el cierre del día anterior. Para cripto se usa
   la vela diaria UTC de Binance. Para acciones se usa el cierre ajustado de Yahoo Finance.
3. Un evento pierde peso con el tiempo: a un año pesa la mitad (`VIDA_MEDIA_AÑOS`). La influencia de una persona cambia.
4. `puntaje = movimiento medio con pesos × confianza`. La confianza baja si la persona tiene pocos eventos o si sus
   eventos son viejos (`PESO_PARA_CONFIAR`).
5. Una persona sin eventos medidos queda «sin medir», al final del ranking.

## Lo que se ve en los datos (noviembre de 2026)

- **El salto de un post casi siempre ocurre en minutos, y una parte se pierde el mismo día.** Ejemplos: con el indulto a
  CZ, BNB llegó a subir cerca de 15 %, pero el día cerró en +5 %. Con «Maybe next year» de Musk, DOGE llegó a subir 8 %,
  pero el día cerró en −2 %. Un robot que mira velas diarias, o que compra después de leer la noticia, llega tarde.
- **Las noticias de estructura duran más que los posts.** Duraron más de 20 días la compra de BTC de Tesla, el fin de los
  pagos en BTC, la caída de FTX, la elección de 2024 y DeepSeek. No duraron la reserva cripto de Trump (+9,5 % el día y
  −2,6 % a los 20 días) ni el arancel de 100 % a China en acciones.
- **La influencia de Musk sobre DOGE bajó mucho** entre 2021 y 2026. La de Trump sobre BTC y el S&P 500 subió.

## Cómo se actualiza

Cada día:
1. Buscar noticias del día anterior donde una persona de la lista movió el precio más de 3 % en cripto o más de 1,5 % en
   acciones.
2. Agregar el evento con su fecha y su fuente en `eventos.json`.
3. Correr `python3 herramientas/medir.py --guardar` y `python3 herramientas/ranking.py`.
4. Si no hay nada nuevo, no se cambia nada.

## Lo que todavía no hace

- No lee las redes sociales directo. X cobra por su API y Truth Social no tiene una API pública. Los eventos salen de
  noticias con fecha.
- Con velas diarias no se ve el minuto exacto del post. Para medir la reacción en minutos hacen falta velas de 1 minuto
  del momento.
- Los roles marcados «revisar» todavía no tienen fuente.

## Licencia de los datos

Los precios son públicos (Binance y Yahoo Finance). Cada evento enlaza su fuente.
