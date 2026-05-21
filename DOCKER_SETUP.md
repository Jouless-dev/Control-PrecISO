# Configuración Docker — Control-PrecISO

## Requisitos

1. [Docker Desktop](https://www.docker.com/products/docker-desktop/) para Windows
2. **WSL2** con una distribución (p. ej. Ubuntu): `wsl --install -d Ubuntu`
3. Reinicio de Windows si el instalador de WSL lo solicita

## Arrancar la aplicación

```powershell
cd D:\Universidad\Control-PrecISO-main
.\serve-docker.ps1
```

URL: **http://localhost:8080**

## Error: "Virtualization support not detected"

1. Activar en BIOS: **Intel VT-x** / **AMD-V**
2. En PowerShell **como administrador**:

```powershell
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

3. Reiniciar el PC
4. `wsl --install -d Ubuntu`
5. Abrir Docker Desktop y esperar a que indique *Running*

## Error: WSL "Class not registered"

```powershell
winget install -e --id Microsoft.WSL --accept-package-agreements
wsl --install -d Ubuntu
```

Reiniciar si es necesario.

## Comandos útiles

| Acción | Comando |
|--------|---------|
| Ver contenedor | `docker ps` |
| Logs | `docker compose logs -f` |
| Detener | `docker compose down` |
| Reconstruir | `docker compose up --build -d` |

## Alternativa sin Docker

```powershell
cd Control-PrecISO-main
python -m http.server 8080
```

Misma URL; útil si el hipervisor no está disponible en el equipo.
