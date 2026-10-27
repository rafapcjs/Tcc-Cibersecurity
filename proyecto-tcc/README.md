# Proyecto TCC — Seguridad Informática

**Universidad de Cartagena · Programas a Distancia**
**Tema:** Seguridad Web (OWASP Top 10) + Criptografía aplicada
**Caso:** Auditoría de una aplicación web vulnerable en laboratorio aislado

---

## ¿De qué trata el proyecto?

Auditamos una aplicación web deliberadamente vulnerable (DVWA) montada en un
laboratorio aislado en VirtualBox. Demostramos tres ataques del OWASP Top 10
—**XSS**, **Inyección SQL** y **Fuerza Bruta** sobre el login— y por cada uno
aplicamos su **contramedida**, incluyendo el uso de **criptografía** (hash de
contraseñas con sal, bcrypt) para proteger las credenciales. Cada ataque se
demuestra *antes* (funciona) y *después* (ya no funciona) de la mitigación.

> **Dos enfoques del curso:** (1) Seguridad Web / OWASP Top 10 y (2) Criptografía
> aplicada. El segundo nace de la mitigación del primero: las defensas contra
> fuerza bruta y robo de credenciales se apoyan en hashing con sal.

## Regla de oro: todo en laboratorio aislado

- Red **solo-anfitrión (Host-Only)** en VirtualBox. Nada se expone a Internet ni
  a la red de casa.
- Objetivo **deliberadamente vulnerable** (DVWA). **Nunca** se prueba contra un
  sitio, IP o empresa real.
- Cada ataque existe para **entenderlo y defenderlo**. Por cada vulnerabilidad,
  su contramedida documentada.

## Integrantes de la CIPA

| Rol | Nombre | Responsabilidad principal |
|---|---|---|
| Líder / documentación | Rafael Alfonso Corredor Gambín | Coordina y arma el documento final |
| Montaje de laboratorio | Nelson Ruiz Marimón | Docker, Kali, DVWA, red aislada |
| Ofensiva (ataques) | John Fredy Morales Revueltas | XSS, SQLi, fuerza bruta + evidencia |
| Defensa (mitigación) y evidencias | Nilson Ruiz Marimón | Contramedidas, scripts de cripto, capturas |

> Propuesta de roles — ajústenla a gusto del equipo. La sustentación (10 min)
> exige explicar quién hizo qué.

## Fechas (del enunciado)

| Entrega | Fecha | Estado |
|---|---|---|
| Avance | 31 de octubre de 2026 | En preparación |
| Entrega final | 20 de noviembre de 2026 | Pendiente |
| Sustentación | 21 de noviembre de 2026 | Pendiente |

## Estructura de carpetas

```
proyecto-tcc/
├── README.md              # este archivo
├── documento/             # avance y documento final (según plantilla oficial)
├── diseno/                # arquitectura, flujo de datos + STRIDE, controles
├── laboratorio/           # guía de montaje de las VMs y la red
├── scripts/               # demos de criptografía (hash de contraseñas)
├── evidencias/
│   └── avance/            # capturas, logs y antes/después (ataques + mitigaciones)
└── sustentacion/          # diapositivas y guion (10 min)
```

## Cómo empezar

1. Sigue `laboratorio/guia-montaje-docker.md` (ruta elegida con Docker) para
   dejar el laboratorio listo. La `guia-montaje.md` es la alternativa con VirtualBox.
2. Revisa el diseño en `diseno/`.
3. Ejecuta los ataques y captura evidencia en `evidencias/`.
4. Aplica las mitigaciones y vuelve a probar.
5. Arma el documento en `documento/` siguiendo la plantilla oficial.
