#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo de criptografía aplicada — Protección de contraseñas (TCC Seguridad Web).

Muestra el ANTES y el DESPUÉS de proteger contraseñas:

  1) ANTES  : contraseñas en texto plano -> un volcado de la BD las expone todas,
              y las débiles caen en segundos ante un ataque de diccionario.
  2) DESPUÉS: hash con sal (bcrypt si está instalado; si no, PBKDF2-HMAC-SHA256
              de la librería estándar). Cada contraseña tiene su propia sal, así
              que dos usuarios con la misma clave producen hashes distintos y el
              atacante no puede usar tablas precalculadas (rainbow tables).

Cómo ejecutar en Windows (PowerShell o terminal de Kali):
    py demo_hash_passwords.py          # Windows (lanzador de Python)
    python3 demo_hash_passwords.py     # Linux / Kali

Opcional, para usar bcrypt (recomendado por el curso):
    pip install bcrypt
"""

import hashlib
import hmac
import secrets
import time

# --- Detectar si bcrypt está disponible (recomendado); si no, usar PBKDF2 ---
try:
    import bcrypt
    TIENE_BCRYPT = True
except ImportError:
    TIENE_BCRYPT = False


def hash_con_sal(clave: str):
    """Devuelve (algoritmo, representacion_guardable) para la clave dada."""
    if TIENE_BCRYPT:
        h = bcrypt.hashpw(clave.encode("utf-8"), bcrypt.gensalt())
        return "bcrypt", h.decode("utf-8")
    # Alternativa 100% librería estándar: PBKDF2-HMAC-SHA256 con sal aleatoria
    sal = secrets.token_bytes(16)
    iteraciones = 200_000
    dk = hashlib.pbkdf2_hmac("sha256", clave.encode("utf-8"), sal, iteraciones)
    # Formato guardable: algoritmo$iteraciones$sal$hash  (sal y hash en hex)
    return "pbkdf2", f"pbkdf2_sha256${iteraciones}${sal.hex()}${dk.hex()}"


def verificar(clave: str, guardado: str) -> bool:
    """Verifica una clave contra su hash guardado."""
    if guardado.startswith("$2") and TIENE_BCRYPT:  # bcrypt
        return bcrypt.checkpw(clave.encode("utf-8"), guardado.encode("utf-8"))
    if guardado.startswith("pbkdf2_sha256$"):
        _, iters, sal_hex, hash_hex = guardado.split("$")
        dk = hashlib.pbkdf2_hmac(
            "sha256", clave.encode("utf-8"),
            bytes.fromhex(sal_hex), int(iters)
        )
        return hmac_compare(dk.hex(), hash_hex)
    return False


def hmac_compare(a: str, b: str) -> bool:
    """Comparación en tiempo constante (evita ataques de temporización)."""
    import hmac
    return hmac.compare_digest(a, b)


# --- Datos de ejemplo (usuarios de laboratorio) ---
USUARIOS = {
    "admin":   "password",      # débil, típica
    "gladys":  "123456",        # débil, típica
    "pablo":   "G7!xQ2@mZ9",     # fuerte
}

# Diccionario pequeño que usaría un atacante (ejemplo didáctico)
DICCIONARIO = ["123456", "password", "admin", "qwerty", "123456789",
               "12345", "iloveyou", "111111", "abc123", "colombia"]


def demo_antes():
    print("=" * 70)
    print(" ANTES — Contraseñas en TEXTO PLANO (lo que NO se debe hacer)")
    print("=" * 70)
    print("Así se verían en la base de datos si no se protegen:\n")
    for u, c in USUARIOS.items():
        print(f"  usuario={u:8}  contraseña={c}")
    print("\n  -> Riesgo: quien lea la BD (SQLi, backup robado, insider) obtiene")
    print("     TODAS las contraseñas al instante. Fuga total de credenciales.\n")

    print("  Ataque de diccionario contra el texto plano (trivial):")
    for u, c in USUARIOS.items():
        roto = c in DICCIONARIO
        estado = "ROTA (estaba en el diccionario)" if roto else "no está en el diccionario"
        print(f"    {u:8} -> {estado}")
    print()


def demo_despues():
    algo = "bcrypt" if TIENE_BCRYPT else "PBKDF2-HMAC-SHA256 (bcrypt no instalado)"
    print("=" * 70)
    print(f" DESPUÉS — Hash con SAL usando {algo}")
    print("=" * 70)
    print("Así se guardarían en la base de datos (irreconocibles):\n")

    almacen = {}
    for u, c in USUARIOS.items():
        _, guardado = hash_con_sal(c)
        almacen[u] = guardado
        print(f"  usuario={u:8}\n    {guardado}\n")

    print("  -> Cada hash incluye su propia sal: aunque 'admin' y otro usuario")
    print("     tuvieran la misma clave, sus hashes serían distintos.\n")

    # Demostrar login correcto e incorrecto
    print("  Verificación de login (sin guardar la clave en claro):")
    print(f"    admin + 'password'  -> {verificar('password', almacen['admin'])}  (correcto)")
    print(f"    admin + 'wrong123'  -> {verificar('wrong123', almacen['admin'])}  (rechazado)")
    print()

    # Mostrar el costo de romper el hash (fuerza bruta de diccionario)
    print("  Ataque de diccionario contra los hashes (ahora hay que probar")
    print("  cada palabra re-hasheándola con la sal de cada usuario):")
    for u, guardado in almacen.items():
        inicio = time.perf_counter()
        encontrada = None
        for palabra in DICCIONARIO:
            if verificar(palabra, guardado):
                encontrada = palabra
                break
        dur = (time.perf_counter() - inicio) * 1000
        if encontrada:
            print(f"    {u:8} -> clave débil hallada ('{encontrada}') tras "
                  f"{dur:.1f} ms de cómputo por cuenta")
        else:
            print(f"    {u:8} -> NO hallada con el diccionario ({dur:.1f} ms gastados)")
    print()
    print("  Lección: el hash con sal NO vuelve segura una clave débil que esté")
    print("  en el diccionario, pero (a) obliga a gastar cómputo por cada cuenta,")
    print("  (b) elimina las rainbow tables, y (c) protege las claves fuertes")
    print("  aunque se filtre la base de datos. Por eso se combina con el")
    print("  control de FUERZA BRUTA (límite de intentos) y con políticas de")
    print("  contraseñas robustas.\n")


if __name__ == "__main__":
    demo_antes()
    demo_despues()
    print("=" * 70)
    print(" Fin de la demo. Captura esta salida para la evidencia de criptografía.")
    print("=" * 70)
