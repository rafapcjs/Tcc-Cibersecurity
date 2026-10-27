# Guía de montaje del laboratorio con Docker (ruta elegida)

En lugar de máquinas virtuales usamos **Docker Desktop** (Windows 11). El
laboratorio sigue siendo **aislado**: DVWA solo escucha en `127.0.0.1` (tu propio
equipo) y el atacante (Kali) y la víctima (DVWA) viven en una red Docker privada
llamada `labnet`. Nada se expone a Internet ni a la red de casa.

```
          Red Docker privada "labnet" (bridge)
   ┌──────────────────────────┐     ┌──────────────────────────────┐
   │ Contenedor KALI          │     │ Contenedor DVWA (víctima)    │
   │ (atacante)               │────►│ Apache + PHP + MariaDB       │
   │ sqlmap · hydra · nmap    │     │ http://dvwa/  (interno)      │
   └──────────────────────────┘     └──────────────────────────────┘
                                         │
                                         ▼  publicado solo en el host
                                 http://127.0.0.1:4280  (tu navegador)
```

> **Este laboratorio ya quedó montado y funcionando en tu equipo.** Esta guía
> sirve para reproducirlo, apagarlo/encenderlo y para documentarlo en el TCC.

---

## 1. Requisito

Docker Desktop instalado y corriendo (ya lo tienes: Docker 29.4.1). Comprueba:
```bash
docker --version
```

## 2. Crear la red aislada y levantar DVWA (víctima)

```bash
docker network create labnet
docker run -d --name dvwa --network labnet -p 127.0.0.1:4280:80 vulnerables/web-dvwa
```
- `-p 127.0.0.1:4280:80` → DVWA solo es accesible desde tu propio equipo
  (aislado). Si el 4280 estuviera ocupado, cambia el número.

## 3. Inicializar la base de datos de DVWA

Abre en el navegador **http://127.0.0.1:4280/setup.php** y pulsa
**"Create / Reset Database"**. (Este paso ya se ejecutó; las tablas `users` y
`guestbook` quedaron creadas.)

Credenciales de DVWA: **admin / password**.
Baja la seguridad en el menú **DVWA Security → Low** para las primeras pruebas.

## 4. Levantar Kali (atacante) en la misma red

```bash
docker run -dit --name kali --network labnet kalilinux/kali-rolling bash
docker exec -it kali bash      # entrar al contenedor
# dentro de Kali:
apt update && apt install -y sqlmap hydra nmap wordlists curl
gzip -dk /usr/share/wordlists/rockyou.txt.gz   # descomprimir el diccionario
```

Desde Kali, la víctima se alcanza por su nombre: **http://dvwa/** (no necesitas
IP; Docker resuelve el nombre dentro de `labnet`).

## 5. Herramientas gráficas (Burp Suite / OWASP ZAP)

Para interceptar con interfaz gráfica, instala en **Windows** la versión
gratuita de **Burp Suite Community** o **OWASP ZAP** y apúntalas a
`http://127.0.0.1:4280`. Los ataques por línea de comandos (sqlmap, hydra, nmap)
van desde el contenedor Kali.

## 6. Encender / apagar el laboratorio

```bash
docker stop kali dvwa        # apagar (sin borrar)
docker start kali dvwa       # volver a encender
docker rm -f kali dvwa       # borrar del todo (habría que rehacer el paso 2-4)
```

---

## 7. Evidencia para el avance (31 de octubre)

Ya se generó en `evidencias/avance/`:
- `00-estado-laboratorio.txt` — contenedores, red aislada, conectividad, herramientas.
- `01-sqli-low-exito.txt` — ataque de inyección SQL funcionando (primera prueba técnica).

**Capturas de pantalla que conviene añadir** (hazlas tú desde el navegador):
1. Docker Desktop mostrando los contenedores `dvwa` y `kali` corriendo.
2. DVWA abierto en `http://127.0.0.1:4280` (pantalla de login y/o Welcome).
3. La página *SQL Injection* de DVWA mostrando los usuarios devueltos tras
   escribir `1' OR '1'='1` en el campo *User ID*.

Guárdalas como `.png` en `evidencias/avance/` con nombres claros.
