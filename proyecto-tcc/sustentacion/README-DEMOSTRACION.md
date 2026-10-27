# Guía de demostración en vivo (sustentación)

Esta guía permite **demostrar que todo el proyecto funciona** frente al tutor:
levantar el laboratorio, reproducir los tres ataques, ver sus mitigaciones y
ejecutar la prueba de criptografía. Sigue los pasos en orden; cada uno dice qué
debe pasar.

> **Todo ocurre en un laboratorio aislado** (Docker, solo en `127.0.0.1`). No se
> toca ningún sistema real.

---

## 0. Requisito

Tener **Docker Desktop** abierto y corriendo. Verificar:

```bash
docker --version
```

---

## 1. Encender el laboratorio

```bash
docker start dvwa kali
```

Comprobar que ambos contenedores están arriba:

```bash
docker ps --filter name=dvwa --filter name=kali
```

Debe mostrar `dvwa` (publicado en `127.0.0.1:4280`) y `kali` como *Up*.

> Si fuera la primera vez (contenedores borrados), seguir
> `../laboratorio/guia-montaje-docker.md` para recrearlos.

---

## 2. Abrir DVWA (la aplicación vulnerable)

1. En el navegador: **http://127.0.0.1:4280**
2. Iniciar sesión: usuario **`admin`** · contraseña **`password`**
3. Menú **DVWA Security** → poner en **Low** → *Submit*
   (nivel vulnerable, para demostrar los ataques).

---

## 3. Demostrar los tres ataques (nivel Low)

### 3.1 Inyección SQL
- Menú **SQL Injection**.
- En *User ID* escribir: `1' OR '1'='1` → *Submit*.
- **Resultado esperado:** la página lista **todos los usuarios** (no solo uno).
- Variante (robo de credenciales): `1' UNION SELECT user, password FROM users -- -`
  devuelve usuarios y sus hashes.

### 3.2 Cross-Site Scripting (XSS)
- Menú **XSS (Reflected)**.
- En el campo escribir: `<script>alert('XSS')</script>` → *Submit*.
- **Resultado esperado:** aparece una **ventana emergente** (el script se
  ejecutó). *(En las evidencias usamos una variante que además muestra la cookie
  robada; ver `evidencias/avance/06-xss-ejecutado-navegador.png`.)*

### 3.3 Fuerza bruta
- Menú **Brute Force**.
- Probar **Username: `admin`** / **Password: `password`** → *Login*.
- **Resultado esperado:** *"Welcome to the password protected area admin"* — una
  credencial débil permite el acceso. (El ataque real automatiza miles de
  intentos; ver evidencia `04` y `07`.)

---

## 4. Demostrar las mitigaciones (que ya NO funcionan)

Menú **DVWA Security** → subir a **High** (o **Impossible**) → *Submit*, y
repetir cada ataque:

| Ataque | Al repetirlo en nivel seguro |
|---|---|
| Inyección SQL (nivel *Impossible*) | Devuelve **0 usuarios** (consultas parametrizadas) |
| XSS (nivel *High*) | El `<script>` se **elimina**, no se ejecuta |
| Fuerza bruta (nivel *High*) | El intento automatizado es **rechazado** (token por intento) |

Esto demuestra el par **problema → mitigación**, que es el corazón del trabajo.

---

## 5. Demostrar la criptografía (protección de contraseñas)

```bash
cd ../scripts
py demo_hash_passwords.py       # Windows
# python3 demo_hash_passwords.py   (Linux/Kali)
```

**Resultado esperado:** muestra el **antes** (contraseñas en texto plano, que
caen al instante con un diccionario) y el **después** (hash con sal: cada clave
queda irreconocible y las claves fuertes resisten).

---

## 6. Dónde está la evidencia

Todas las pruebas quedaron guardadas en `../evidencias/avance/`:

| Archivo | Qué muestra |
|---|---|
| `00-estado-laboratorio.txt` | Contenedores y red aislada |
| `01-sqli-low-exito.txt` | Inyección SQL (log) |
| `02-docker-contenedores.png` | Contenedores en Docker |
| `02b-xss-low-exito.txt` | XSS reflejado y almacenado (log) |
| `03-sqli-navegador-usuarios.png` | SQLi en el navegador |
| `04-fuerza-bruta-low-exito.txt` | Fuerza bruta (log) |
| `05-mitigaciones-despues.txt` | Antes → después de las tres |
| `06-xss-ejecutado-navegador.png` | XSS ejecutado leyendo la cookie |
| `07-fuerza-bruta-navegador.png` | Acceso logrado por fuerza bruta |

El documento (`../documento/Avance_TCC.docx`) y las diapositivas
(`Sustentacion_TCC.pptx`) incluyen estas capturas.

---

## 7. Apagar el laboratorio

Al terminar la demostración:

```bash
docker stop dvwa kali
```

Para reanudarlo en otra ocasión: `docker start dvwa kali`.

---

## Consejo

Ensayen la demo una vez antes de la sustentación y **graben un video de respaldo**
de estos pasos, por si el laboratorio en vivo fallara el día de la exposición.
