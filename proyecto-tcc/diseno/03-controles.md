# Artefacto 3 — Propuesta de controles / contramedidas

Tabla `amenaza → control`. Es el mapa que conecta cada ataque demostrado con su
defensa. Cada fila se prueba *antes* (ataque funciona) y *después* (ya no).

| # | Amenaza | Activo afectado | Control / contramedida | Enfoque |
|---|---|---|---|---|
| 1 | **Inyección SQL** en el login y formularios | Base de datos de usuarios | **Consultas parametrizadas** (prepared statements) + validación/escape de entrada | OWASP |
| 2 | **XSS** (reflejado y almacenado) en campos de la web | Sesión del usuario / navegador | **Sanitización de salida** + codificación HTML + cabeceras `Content-Security-Policy` y `X-XSS-Protection` | OWASP |
| 3 | **Fuerza bruta** sobre el login | Credenciales / cuentas | **Límite de intentos** + bloqueo temporal + CAPTCHA + retardo progresivo | OWASP |
| 4 | **Contraseñas en texto plano** en la BD | Credenciales | **Hash con sal** (bcrypt / Argon2) — aunque roben la BD, no obtienen las claves | Criptografía |
| 5 | **Robo de cookie de sesión** vía XSS | Sesión | Atributos de cookie `HttpOnly` y `Secure` | OWASP / Cripto (TLS) |
| 6 | **Falta de trazabilidad** de intentos (repudio) | Auditoría | Registro (logging) de intentos de autenticación fallidos | OWASP |

## Detalle de los controles clave

### Control 1 — Consultas parametrizadas (anti-SQLi)
Nunca concatenar entrada del usuario en el SQL. En PHP/MySQLi o PDO:
```php
// Vulnerable:
$q = "SELECT * FROM users WHERE user='$u' AND pass='$p'";
// Seguro (parametrizado):
$stmt = $pdo->prepare("SELECT * FROM users WHERE user=? AND pass=?");
$stmt->execute([$u, $p]);
```

### Control 2 — Sanitización de salida + CSP (anti-XSS)
Codificar la entrada antes de reflejarla y restringir scripts con CSP:
```php
echo htmlspecialchars($entrada, ENT_QUOTES, 'UTF-8');
header("Content-Security-Policy: default-src 'self'");
```

### Control 3 — Límite de intentos (anti-fuerza bruta)
Bloquear la cuenta/IP tras N intentos fallidos y añadir retardo. En DVWA esto se
observa directamente subiendo el nivel de seguridad a *High*.

### Control 4 — Hash con sal (criptografía aplicada)
El control criptográfico central del proyecto. Guardar solo el hash:
```php
// Al registrar / cambiar contraseña:
$hash = password_hash($clave, PASSWORD_BCRYPT);
// Al verificar:
if (password_verify($clave_ingresada, $hash_guardado)) { /* ok */ }
```
La demostración en `scripts/demo_hash_passwords.py` muestra el **antes**
(texto plano, roto en segundos) y el **después** (bcrypt con sal, inviable).

## Trazabilidad con el documento

- **Problemática / Justificación:** amenazas de la tabla.
- **Solución planteada:** controles 1–6.
- **Resultados:** evidencia antes→después por cada control probado (1, 2, 3, 4).
