# Artefacto 1 — Diagrama de arquitectura segura

Muestra las máquinas virtuales, la red aislada y **dónde vive cada control** de
seguridad (los controles van en el estado *mitigado* del laboratorio).

> Pega este diagrama en draw.io o visualízalo con cualquier visor de Mermaid.
> Para el documento final, expórtalo como imagen a `evidencias/`.

```mermaid
flowchart LR
    subgraph HOST["Equipo anfitrión (Windows 11) — VirtualBox"]
        direction LR
        subgraph NET["Red Host-Only vboxnet0 — 192.168.56.0/24 (AISLADA, sin Internet)"]
            direction LR
            KALI["🖥️ VM ATACANTE — Kali Linux\n192.168.56.10\nBurp Suite · OWASP ZAP\nsqlmap · Hydra · Wireshark"]
            subgraph VICTIM["🖥️ VM VÍCTIMA — DVWA · 192.168.56.20"]
                direction TB
                WAF["Cabeceras de seguridad\n(CSP, X-Frame-Options)\n← control anti-XSS"]
                APP["Aplicación web DVWA\n(PHP)\nValidación/sanitización de entrada\nConsultas parametrizadas ← anti-SQLi\nLímite de intentos ← anti-fuerza bruta"]
                DB["Base de datos MySQL\nContraseñas con hash + sal (bcrypt)\n← criptografía aplicada"]
                WAF --> APP --> DB
            end
            KALI -->|"HTTP de laboratorio\n(interceptado con Burp)"| VICTIM
        end
    end

    classDef ctrl fill:#1f6feb22,stroke:#1f6feb,color:#0b3d91;
    class WAF,APP,DB ctrl;
```

## Lectura del diagrama

- **Todo ocurre dentro del equipo anfitrión**, en una red Host-Only que no sale
  a Internet ni toca la red real.
- La **VM atacante (Kali)** envía las peticiones de prueba y las intercepta con
  Burp Suite / ZAP.
- La **VM víctima (DVWA)** es el objetivo deliberadamente vulnerable. Sobre ella
  colocamos los controles en la fase de mitigación:
  - **Cabeceras de seguridad** (capa del servidor web) → mitigan **XSS**.
  - **Validación de entrada + consultas parametrizadas** (capa de aplicación) →
    mitigan **Inyección SQL**.
  - **Límite de intentos / bloqueo** (capa de aplicación) → mitiga **fuerza bruta**.
  - **Hash con sal (bcrypt)** en la base de datos → protege las credenciales aun
    si la BD se ve comprometida (**criptografía aplicada**).

## Nota sobre la arquitectura (estado vulnerable vs. mitigado)

En la fase 1 (ataque) la VM víctima corre **sin** estos controles (DVWA en nivel
*Low*). En la fase 2 (mitigación) activamos los controles (DVWA en nivel *High*
y/o cambios de configuración) y repetimos los ataques para demostrar que ya no
funcionan. Ese par **antes → después** es el corazón de la evidencia.
