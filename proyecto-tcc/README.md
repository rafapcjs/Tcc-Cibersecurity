# Proyecto TCC — Seguridad Informática

**Universidad de Cartagena · Programas a Distancia**
**Tema:** Seguridad Web (OWASP Top 10) + Criptografía aplicada
**Caso:** Auditoría de una aplicación web vulnerable en laboratorio aislado
**Repositorio:** https://github.com/rafapcjs/Tcc-Cibersecurity

---

## ¿De qué trata el proyecto?

Auditamos una aplicación web deliberadamente vulnerable (DVWA) montada en un
laboratorio aislado con **Docker**. Demostramos tres ataques del OWASP Top 10
—**Inyección SQL**, **XSS** y **Fuerza Bruta** sobre el login— y por cada uno
aplicamos su **contramedida**, incluyendo el uso de **criptografía** (hash de
contraseñas con sal, bcrypt/Argon2) para proteger las credenciales. Cada ataque
se demuestra *antes* (funciona) y *después* (ya no funciona) de la mitigación.

> **Dos enfoques del curso:** (1) Seguridad Web / OWASP Top 10 y (2) Criptografía
> aplicada. El segundo nace de la mitigación del primero: las defensas contra
> fuerza bruta y robo de credenciales se apoyan en hashing con sal.

## Regla de oro: todo en laboratorio aislado

- Red **privada** en Docker; DVWA publicado solo en `127.0.0.1`. Nada se expone a
  Internet ni a la red de casa.
- Objetivo **deliberadamente vulnerable** (DVWA). **Nunca** se prueba contra un
  sitio, IP o empresa real.
- Cada ataque existe para **entenderlo y defenderlo**. Por cada vulnerabilidad,
  su contramedida documentada.

## Estado del proyecto

Todos los componentes están **completos y verificados**:

- ✅ **Documento** según la plantilla oficial (3.000+ palabras, con figuras de evidencia).
- ✅ **Laboratorio Docker** funcionando (Kali atacante + DVWA víctima, red aislada).
- ✅ **Los 3 ataques demostrados** con su mitigación (evidencia antes → después).
- ✅ **Script de criptografía** probado (texto plano vs. hash con sal).
- ✅ **3 artefactos de diseño** (arquitectura, flujo + STRIDE, controles).
- ✅ **Análisis de riesgos MAGERIT** (enfoque complementario) + matriz en Excel.
- ✅ **Diapositivas + guion** de la sustentación (10 min).
- ✅ **Guía de demostración en vivo** para la sustentación.

## Integrantes de la CIPA

| Rol | Nombre | Responsabilidad principal |
|---|---|---|
| Líder / documentación | Rafael Alfonso Corredor Gambín | Coordina y arma el documento final |
| Montaje de laboratorio | Nelson Ruiz Marimón | Docker, Kali, DVWA, red aislada |
| Ofensiva (ataques) | John Fredy Morales Revueltas | XSS, SQLi, fuerza bruta + evidencia |
| Defensa (mitigación) y evidencias | Nilson Ruiz Marimón | Contramedidas, scripts de cripto, capturas |

**Tutor:** Rafael Enrique Benedetti Navarro

> Propuesta de roles — ajústenla a gusto del equipo. La sustentación (10 min)
> exige explicar quién hizo qué.

## Fechas (del enunciado)

| Entrega | Fecha | Estado |
|---|---|---|
| Avance | 31 de octubre de 2026 | ✅ Listo |
| Entrega final | 20 de noviembre de 2026 | ✅ Material listo |
| Sustentación | 21 de noviembre de 2026 | ✅ Diapositivas y guion listos |

## Estructura de carpetas

```
proyecto-tcc/
├── README.md                       # este archivo
├── documento/
│   └── Avance_TCC.docx             # documento del TCC (plantilla oficial)
├── diseno/
│   ├── 01-arquitectura-segura.md
│   ├── 02-flujo-datos-amenazas-STRIDE.md
│   └── 03-controles.md
├── analisis-riesgos/
│   ├── analisis-de-riesgos-MAGERIT.md   # metodología MAGERIT / ISO 27005
│   └── matriz-de-riesgos.xlsx           # matriz probabilidad × impacto
├── laboratorio/
│   ├── guia-montaje-docker.md      # ruta elegida (Docker)
│   ├── guia-montaje.md             # alternativa (VirtualBox)
│   └── playbook-ataques-mitigacion.md
├── scripts/
│   ├── demo_hash_passwords.py      # criptografía: hash con sal (probado)
│   └── README.md
├── evidencias/
│   └── avance/                     # 11 evidencias (recon, capturas, logs, antes/después)
└── sustentacion/
    ├── Sustentacion_TCC.pptx       # 11 diapositivas con capturas
    ├── guion-sustentacion.md       # guion con tiempos y reparto
    └── README-DEMOSTRACION.md      # guía para demostrar en vivo ante el tutor
```

## Cómo demostrar que todo funciona (sustentación)

Sigue **`sustentacion/README-DEMOSTRACION.md`** — guía paso a paso para enseñarle
al tutor, en vivo, que el proyecto funciona. En resumen:

1. Enciende el laboratorio: `docker start dvwa kali`
2. Abre DVWA: http://127.0.0.1:4280 (usuario `admin` / contraseña `password`)
3. Demuestra los 3 ataques (SQLi, XSS, fuerza bruta) en nivel *Low*.
4. Sube la seguridad a *High*/*Impossible* y repítelos: ya no funcionan.
5. Corre la prueba de criptografía: `py scripts/demo_hash_passwords.py`
6. Apaga el laboratorio: `docker stop dvwa kali`

## Cómo está construido (para reproducirlo desde cero)

1. Monta el laboratorio con `laboratorio/guia-montaje-docker.md`.
2. Revisa el diseño en `diseno/`.
3. Ejecuta los ataques del `laboratorio/playbook-ataques-mitigacion.md` y guarda
   la evidencia en `evidencias/avance/`.
4. Aplica las mitigaciones y vuelve a probar (antes → después).
5. El documento está en `documento/` siguiendo la plantilla oficial.
