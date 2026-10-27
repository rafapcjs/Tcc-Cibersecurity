# Guía de montaje del laboratorio aislado

Equipo base: **Windows 11**. Montamos dos máquinas virtuales en una red
**Host-Only** (aislada), sin acceso a Internet entre ellas ni exposición a la
red real.

```
                 Red Host-Only (vboxnet0) — 192.168.56.0/24
      ┌─────────────────────────────┐        ┌─────────────────────────────┐
      │  VM ATACANTE — Kali Linux   │        │  VM VÍCTIMA — DVWA          │
      │  192.168.56.10              │◄──────►│  192.168.56.20              │
      │  Burp, ZAP, Hydra, sqlmap   │        │  Apache + PHP + MySQL (DVWA)│
      └─────────────────────────────┘        └─────────────────────────────┘
```

> **Importante:** la red **Host-Only no sale a Internet**. Para *descargar* las
> ISO/OVA y actualizar Kali al inicio puedes usar temporalmente NAT; al terminar,
> deja **solo** el adaptador Host-Only activo para las pruebas.

---

## 0. Requisitos del equipo anfitrión

- Windows 11 con **virtualización habilitada** en BIOS/UEFI (VT-x / AMD-V).
- Mínimo **8 GB de RAM** (ideal 16) y ~40 GB libres en disco.
- Si tienes **Hyper-V / WSL2 / Docker Desktop** activos, pueden chocar con
  VirtualBox. Si VirtualBox da error de VT-x, desactiva Hyper-V:
  ```powershell
  # PowerShell como Administrador
  bcdedit /set hypervisorlaunchtype off
  # reinicia el equipo
  ```
  (Para revertir: `bcdedit /set hypervisorlaunchtype auto`)

---

## 1. Instalar VirtualBox

1. Descarga **VirtualBox** (Windows hosts) y el **Extension Pack** desde
   https://www.virtualbox.org/wiki/Downloads
2. Instala VirtualBox con las opciones por defecto.
3. Instala el Extension Pack (doble clic sobre el archivo descargado).

---

## 2. Crear la red aislada (Host-Only)

En VirtualBox: **Herramientas → Administrador de red → Redes solo anfitrión →
Crear**. Debe quedar algo como `VirtualBox Host-Only Ethernet Adapter`
(vboxnet0) con rango `192.168.56.0/24`. Deja el servidor **DHCP habilitado** o
asigna IP estática a cada VM (lo hacemos abajo).

---

## 3. VM Atacante — Kali Linux (la forma más rápida)

1. Descarga la imagen **prearmada para VirtualBox** (archivo `.7z` que contiene
   un `.vbox` + `.vdi`) desde https://www.kali.org/get-kali/#kali-virtual-machines
2. Descomprime y haz **Archivo → Importar** (o abre el `.vbox`).
3. Credenciales por defecto: usuario `kali`, contraseña `kali`.
4. **Red de la VM:** Configuración → Red →
   - Adaptador 1: **Solo-anfitrión (Host-Only)** → `vboxnet0`
   - (Opcional, solo para descargar/actualizar) Adaptador 2: NAT
5. Arranca Kali y actualiza + instala herramientas:
   ```bash
   sudo apt update && sudo apt -y full-upgrade
   sudo apt -y install wireshark burpsuite zaproxy hydra sqlmap nmap
   ```
   (Burp Suite y OWASP ZAP suelen venir preinstalados en Kali; el comando los
   asegura.)

---

## 4. VM Víctima — DVWA

Tienes **dos opciones**. La **A** es la más rápida y la recomendada para el
avance; la **B** es más "de libro" si quieres una VM dedicada.

### Opción A (recomendada): DVWA en Docker, dentro de una VM ligera

En una VM **Ubuntu Server** mínima (o incluso en la propia Kali si el tiempo
apremia), instala Docker y levanta DVWA con un solo comando:

```bash
sudo apt update && sudo apt -y install docker.io
sudo systemctl enable --now docker
sudo docker run -d -p 80:80 --name dvwa vulnerables/web-dvwa
```

DVWA queda en `http://<IP-de-la-VM>/`. Login por defecto: `admin` / `password`.
En la primera pantalla pulsa **Create / Reset Database**.

### Opción B: Metasploitable 2 (DVWA ya incluido, sin Docker)

1. Descarga **Metasploitable 2** (imagen de práctica clásica, trae DVWA
   preinstalado) desde SourceForge (busca "Metasploitable2").
2. Descomprime y crea una VM Linux de 64 MB–512 MB usando el `.vmdk` como disco
   existente.
3. Red: **Solo-anfitrión (Host-Only)** → `vboxnet0`.
4. Credenciales: `msfadmin` / `msfadmin`.
5. DVWA queda en `http://<IP>/dvwa/`.

---

## 5. Fijar IPs y verificar conectividad aislada

En Kali, confirma su IP de la red Host-Only:
```bash
ip a | grep 192.168.56
```

Desde Kali, haz ping a la víctima:
```bash
ping -c 3 192.168.56.20
```

Abre DVWA desde el navegador de Kali: `http://192.168.56.20/` (Opción A) o
`http://192.168.56.20/dvwa/` (Opción B).

Baja el nivel de seguridad de DVWA a **Low** (menú *DVWA Security*) para la
primera demostración de los ataques; luego lo subiremos a **High** para mostrar
que las mitigaciones funcionan.

---

## 6. Evidencia mínima para el avance (31 de octubre)

Guarda en `evidencias/avance/` capturas de:

1. VirtualBox con las dos VMs creadas.
2. La red Host-Only configurada.
3. Kali arrancada (pantalla de escritorio o `ip a`).
4. DVWA abierto en el navegador de Kali (pantalla de login).
5. `ping` exitoso entre Kali y la víctima.

Con esto ya tienes la *evidencia mínima de avance técnico* que pide el enunciado.

---

## Solución de problemas frecuentes

- **VirtualBox dice "VT-x no disponible":** habilita virtualización en BIOS y/o
  desactiva Hyper-V (ver sección 0).
- **No hay conectividad entre VMs:** verifica que ambas tengan el adaptador
  Host-Only en la **misma** red `vboxnet0`.
- **DVWA no carga:** en Opción A revisa `sudo docker ps`; en Opción B revisa que
  Apache y MySQL estén arriba (`service apache2 status`).
