# Scripts

## demo_hash_passwords.py — Criptografía aplicada (protección de contraseñas)

Demuestra el **antes** (contraseñas en texto plano) y el **después** (hash con
sal) para el enfoque de criptografía del proyecto.

### Ejecutar

```bash
# Windows (PowerShell / terminal):
py demo_hash_passwords.py

# Linux / Kali:
python3 demo_hash_passwords.py
```

Funciona **sin instalar nada** (usa PBKDF2-HMAC-SHA256 de la librería estándar).
Para usar **bcrypt** (recomendado por el curso) instala la librería y el script
lo detecta solo:

```bash
pip install bcrypt
```

### Qué demuestra

1. Que en texto plano las contraseñas se leen y rompen al instante.
2. Que con hash+sal cada clave queda irreconocible y con sal única.
3. Que el login sigue funcionando sin guardar la clave en claro
   (`password_verify`).
4. Que el hash+sal obliga al atacante a gastar cómputo por cada cuenta y protege
   las claves fuertes aun si se filtra la base de datos.

Captura la salida del script como evidencia del enfoque de criptografía.
