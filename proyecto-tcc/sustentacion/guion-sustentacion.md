# Guion de sustentación (10 minutos)

Orden exigido por el curso, con tiempos. Cada diapositiva trae además notas del
orador (visibles en PowerPoint en la vista de presentador).

| # | Diapositiva | Tiempo | Quién | Mensaje clave |
|---|---|---|---|---|
| 1 | Portada | 0:30 | Líder | Saludo, equipo, tema |
| 2 | El problema | 1:00 | — | PyME con portal inseguro; riesgo legal (Ley 1581) |
| 3 | La solución planteada | 1:00 | — | OWASP + criptografía; regla de oro: lab aislado |
| 4 | El laboratorio (Docker) | 1:00 | Montaje | Kali ataca a DVWA en red privada aislada |
| 5 | Prueba 1 — SQL Injection | 1:30 | Ofensiva | `1' OR '1'='1` → 5 usuarios; mitigado → 0 |
| 6 | Prueba 2 — XSS | 1:30 | Ofensiva | `<script>` ejecutado; mitigado → neutralizado |
| 7 | Prueba 3 — Fuerza bruta | 1:30 | Ofensiva | halló admin/password; mitigado → acceso denegado |
| 8 | Criptografía | 1:00 | Defensa | MD5 sin sal vs. bcrypt con sal |
| 9 | Vulnerabilidades → mitigaciones | 1:00 | Defensa | Tabla resumen antes→después |
| 10 | Distribución de roles | 1:00 | Todos | Quién hizo qué |
| 11 | Conclusiones | 0:30 | Líder | Mensaje final + preguntas |

**Total:** ~10:30 (deja margen; ajusten recortando en 5–7).

## Reparto sugerido de la exposición

- **Rafael (líder):** portada, solución y conclusiones.
- **Nelson (montaje):** el laboratorio Docker.
- **John Fredy (ofensiva):** las tres pruebas de ataque.
- **Nilson (defensa):** criptografía y tabla de mitigaciones.

## Consejos

- **Graben la demo** (una captura de pantalla en video de los 3 ataques en DVWA)
  como respaldo, por si el laboratorio en vivo falla.
- Si hacen demo en vivo: tengan el lab encendido antes (`docker start dvwa kali`)
  y DVWA abierto en `http://127.0.0.1:4280` con sesión iniciada.
- Hablen del **par problema → mitigación**: es lo que más valora el curso.
- Ensayen una vez con cronómetro; 10 minutos pasan rápido.
