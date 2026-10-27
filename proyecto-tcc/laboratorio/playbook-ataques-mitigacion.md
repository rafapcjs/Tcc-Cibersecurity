# Playbook de ataques y mitigación (sobre DVWA, en laboratorio)

Para **cada** ataque: primero se demuestra que funciona (DVWA en nivel *Low*),
se explica la causa, se aplica la mitigación y se vuelve a probar (DVWA en nivel
*High*) para mostrar que ya **no** funciona. Captura evidencia en cada paso y
guárdala en `evidencias/` con nombres claros (ej. `01-sqli-low-exito.png`,
`01-sqli-high-bloqueado.png`).

> Recordatorio: todo esto se hace **solo** contra la VM víctima del laboratorio
> (DVWA), nunca contra un sitio real.

---

## Ataque 1 — Inyección SQL (SQL Injection)

**Dónde:** DVWA → *SQL Injection*.

**Demostración (nivel Low):**
En el campo *User ID* escribe:
```
1' OR '1'='1
```
Debe devolver todos los usuarios. Para extraer usuarios y hashes:
```
1' UNION SELECT user, password FROM users -- -
```
También puedes automatizarlo desde Kali con sqlmap (capturando antes la cookie
de sesión de DVWA):
```bash
sqlmap -u "http://192.168.56.20/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="PHPSESSID=XXXX; security=low" --batch --dump -T users
```

**Causa:** la entrada del usuario se concatena directamente en la consulta SQL.

**Mitigación:** consultas parametrizadas (prepared statements) + validación de
entrada. En DVWA, sube la seguridad a *High* y repite: el payload ya no extrae
datos.

**Evidencia:** captura del `OR '1'='1` funcionando (Low) y bloqueado (High).

---

## Ataque 2 — Cross-Site Scripting (XSS)

**Dónde:** DVWA → *XSS (Reflected)* y *XSS (Stored)*.

**Demostración (nivel Low):**
En el campo de texto escribe:
```html
<script>alert('XSS')</script>
```
Debe aparecer la ventana emergente. Para demostrar robo de sesión (didáctico):
```html
<script>document.write(document.cookie)</script>
```

**Causa:** la aplicación refleja/almacena la entrada sin sanitizarla y el
navegador la ejecuta como código.

**Mitigación:** codificación de salida (`htmlspecialchars`), cabecera
`Content-Security-Policy`, y cookies con `HttpOnly`. En DVWA, nivel *High*: el
script se muestra como texto, no se ejecuta.

**Evidencia:** captura del `alert('XSS')` ejecutándose (Low) y neutralizado (High).

---

## Ataque 3 — Fuerza bruta en el login (Brute Force)

**Dónde:** DVWA → *Brute Force*.

**Demostración (nivel Low):** con Hydra desde Kali, probando un diccionario de
contraseñas contra el usuario `admin` (ajusta la cookie y la cadena de fallo):
```bash
hydra 192.168.56.20 http-get-form \
  "/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:Username and/or password incorrect:H=Cookie: PHPSESSID=XXXX; security=low" \
  -l admin -P /usr/share/wordlists/rockyou.txt -t 4
```
(En Kali, descomprime primero: `sudo gzip -d /usr/share/wordlists/rockyou.txt.gz`.)
Alternativa gráfica: Burp Suite → *Intruder* con la misma lista.

**Causa:** no hay límite de intentos ni bloqueo; se pueden probar miles de
contraseñas automáticamente. Agravado si las claves son débiles.

**Mitigación:**
- Límite de intentos + bloqueo temporal de cuenta/IP (nivel *High* en DVWA
  añade un retardo que frena a Hydra).
- CAPTCHA.
- **Contraseñas con hash y sal** (bcrypt) para que, aun si roban la BD vía SQLi,
  no obtengan las claves en claro → ver `scripts/demo_hash_passwords.py`.

**Evidencia:** captura de Hydra encontrando la clave (Low) y fallando/ralentizado
(High); salida del script de hashing mostrando antes→después.

---

## Resumen de evidencia a capturar (para la entrega final)

| Ataque | Antes (vulnerable) | Después (mitigado) |
|---|---|---|
| SQL Injection | datos extraídos con `OR '1'='1` / sqlmap | payload sin efecto en *High* |
| XSS | `alert('XSS')` ejecutado | script mostrado como texto |
| Fuerza bruta | Hydra/Burp halla la clave | intentos bloqueados/ralentizados |
| Criptografía | contraseñas en texto plano | hashes con sal (salida del script) |
