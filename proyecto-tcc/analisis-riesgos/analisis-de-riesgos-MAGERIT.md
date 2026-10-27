# Análisis de riesgos — Metodología MAGERIT

Tercer enfoque del proyecto (complementario a OWASP y Criptografía). Aplica la
metodología **MAGERIT** (alineada con ISO 27005) al caso de la aplicación web de
la PyME, para identificar y tratar los riesgos de forma estructurada.

> MAGERIT = Metodología de Análisis y Gestión de Riesgos de los Sistemas de
> Información. Pasos: (1) inventario de activos, (2) identificación de amenazas y
> vulnerabilidades, (3) valoración del riesgo (probabilidad × impacto), y
> (4) tratamiento (controles para los riesgos altos).

La matriz cuantitativa está en `matriz-de-riesgos.xlsx`.

---

## 1. Inventario y valoración de activos

| ID | Activo | Tipo | Valor | Justificación |
|---|---|---|---|---|
| A1 | Base de datos de usuarios | Datos | **Alto** | Contiene credenciales y datos personales de clientes |
| A2 | Aplicación web (portal) | Software | **Alto** | Es el servicio de negocio; su caída o compromiso afecta a todos |
| A3 | Credenciales de usuarios | Datos | **Alto** | Su robo permite suplantación y accesos no autorizados |
| A4 | Sesiones de usuario | Datos | Medio | Su secuestro permite actuar como el usuario legítimo |
| A5 | Servidor web (Apache) | Hardware/SW | Medio | Soporta la aplicación; un fallo interrumpe el servicio |
| A6 | Datos personales de clientes | Datos | **Alto** | Protegidos por la Ley 1581 de 2012; su fuga acarrea sanciones |

## 2. Amenazas y vulnerabilidades por activo

| Amenaza | Activos afectados | Vulnerabilidad que la habilita |
|---|---|---|
| Inyección SQL | A1, A3, A6 | Entrada concatenada en la consulta sin parametrizar |
| Cross-Site Scripting (XSS) | A4, A2 | Salida no sanitizada / sin codificar |
| Fuerza bruta en el login | A3 | Sin límite de intentos y contraseñas débiles |
| Robo de credenciales por filtración | A3, A1 | Contraseñas en texto plano / MD5 sin sal |
| Secuestro de sesión | A4 | Cookies sin HttpOnly, XSS activo |
| Fuga de datos personales | A6 | Suma de las anteriores (acceso a la BD) |

## 3. Valoración del riesgo (probabilidad × impacto)

Escala: Probabilidad e Impacto en 1 (bajo), 2 (medio), 3 (alto).
**Riesgo = Probabilidad × Impacto** → 1–2 Bajo · 3–4 Medio · 6–9 Alto.

| Riesgo | Prob. | Impacto | Nivel | 
|---|:---:|:---:|:---:|
| R1 — Inyección SQL | 3 | 3 | **9 · Alto** |
| R2 — XSS | 3 | 2 | **6 · Alto** |
| R3 — Fuerza bruta | 3 | 2 | **6 · Alto** |
| R4 — Credenciales en texto plano/MD5 | 2 | 3 | **6 · Alto** |
| R5 — Secuestro de sesión | 2 | 2 | 4 · Medio |
| R6 — Fuga de datos personales | 2 | 3 | **6 · Alto** |

## 4. Tratamiento de los riesgos (controles)

Para cada riesgo **Alto** se define el control que lo reduce. El tratamiento
elegido es **mitigar** (reducir probabilidad y/o impacto).

| Riesgo | Tratamiento | Control aplicado | Riesgo residual |
|---|---|---|---|
| R1 SQLi | Mitigar | Consultas parametrizadas + validación de entrada | Bajo |
| R2 XSS | Mitigar | Codificación de salida + CSP + cookies HttpOnly | Bajo |
| R3 Fuerza bruta | Mitigar | Límite de intentos + bloqueo + CAPTCHA | Bajo |
| R4 Credenciales | Mitigar | Hash con sal (bcrypt/Argon2) | Bajo |
| R6 Fuga de datos | Mitigar | Suma de R1–R4 + cifrado y mínimos privilegios | Bajo |
| R5 Sesión | Mitigar | HttpOnly/Secure + TLS | Bajo |

## 5. Conclusión del análisis

El análisis MAGERIT confirma que los riesgos más altos del sistema (R1, R2, R3,
R4 y R6) coinciden con las vulnerabilidades que el proyecto demuestra y mitiga en
el laboratorio. Tras aplicar los controles, el riesgo residual de cada uno baja a
**nivel Bajo**, lo que valida la estrategia de seguridad propuesta y conecta el
análisis de riesgos con la implementación práctica (OWASP + criptografía).
