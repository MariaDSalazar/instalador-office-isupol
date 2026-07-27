# Instalador de Office · ISUPOL

**Instituto Superior Tecnológico Policía Nacional**
Tecnología Superior Universitaria en Prevención del Delito y Seguridad Ciudadana

| | |
|---|---|
| **Asignatura** | Competencias Digitales · Unidad 1 de 3 |
| **Docente** | Mgtr. María del Carmen Salazar Torres |
| **Curso / Paralelo** | Sección C |

Instala Microsoft Office descargándolo **directamente de los servidores de Microsoft**
(`officecdn.microsoft.com` y `c2rsetup.officeapps.live.com`). No usa páginas de terceros
ni archivos de dudosa procedencia.

Material educativo para practicar en un entorno de laboratorio.

![Menú del instalador](capturas/pantalla-p1.png)

---

## Cómo se usa

Abra **PowerShell como administrador** — tecla <kbd>Windows</kbd> → escriba `PowerShell`
→ *Ejecutar como administrador* → **Sí** — y pegue esta línea con clic derecho:

```powershell
irm https://raw.githubusercontent.com/MariaDSalazar/instalador-office-isupol/main/office-isupol.ps1 | iex
```

Pulse <kbd>Enter</kbd> y aparecerá el menú. A partir de ahí todo se elige escribiendo un
número.

> **Importante:** debe ser PowerShell *como administrador*. Sin esos permisos el
> instalador se detiene con un aviso en rojo.

## El menú

| Opción | Qué hace |
|:---:|---|
| **1** | Office 2016 Professional Plus — suite completa |
| **2** | Office 2019 Professional Plus — Word, Excel, PowerPoint |
| **3** | Office LTSC 2021 Professional Plus — Word, Excel, PowerPoint |
| **4** | Office LTSC 2024 Professional Plus — Word, Excel, PowerPoint |
| **5** | Activar con MAS ([massgrave.dev](https://massgrave.dev)) |
| **6** | Ver qué Office hay instalado y su estado de licencia |
| **7** | Desinstalar Office |
| **8** | Ayuda dentro del propio programa |
| **9** | Salir |

En la opción **7** los números están invertidos a propósito: el **1 cancela** y solo el
**2** borra, para que nadie desinstale Office por inercia.

## Requisitos

- Windows 10 (build 10240) o Windows 11
- Permisos de administrador
- 5 GB libres en el disco del sistema
- Conexión a internet

El script comprueba los cuatro al arrancar y avisa si falta alguno.

## Manual para principiantes

**[MANUAL-Instalar-Office.pdf](MANUAL-Instalar-Office.pdf)** — 16 páginas, 22 figuras con
flechas rojas. Explica todo desde encender la computadora hasta comprobar que Office quedó
activado, sin dar nada por sabido. Incluye glosario ilustrado y una sección con los errores
más frecuentes.

## Si algo falla

| Mensaje | Solución |
|---|---|
| `...la ejecución de scripts está deshabilitada en este sistema` | Ejecute `Set-ExecutionPolicy Bypass -Scope Process -Force` y vuelva a pegar el comando. Solo afecta a esa ventana. |
| `'irm' no se reconoce como un comando interno o externo` | El comando se pegó en CMD. Debe usarse **PowerShell** (fondo azul oscuro, título `PS C:\...`). |
| `No se puede establecer un canal seguro para SSL/TLS` | Windows sin actualizar. El script ya fuerza TLS 1.2; si aun así falla, ejecute antes `[Net.ServicePointManager]::SecurityProtocol = 'Tls12'`. |
| `FALTAN PERMISOS DE ADMINISTRADOR` | PowerShell se abrió con «Abrir» en vez de «Ejecutar como administrador». |

El manual desarrolla cada uno con el texto exacto del error y capturas.

## Detalles técnicos

| Versión | Product ID | Canal / método |
|---|---|---|
| 2016 | `ProPlusRetail` | `c2rsetup.officeapps.live.com` (`version=O16GA`) |
| 2019 | `ProPlus2019Volume` | `PerpetualVL2019` (ODT) |
| 2021 | `ProPlus2021Volume` | `PerpetualVL2021` (ODT) |
| 2024 | `ProPlus2024Volume` | `PerpetualVL2024` (ODT) |

Office 2016 no existe en el Office Deployment Tool moderno, por eso va por otra ruta. Esa
vía no permite excluir aplicaciones, así que instala la suite entera. Las demás versiones
quedan solo con Word, Excel y PowerPoint: el resto se excluye vía `<ExcludeApp>`.

## Antivirus

El instalador no debería dar problemas: descarga de dominios de Microsoft y no hace nada
ofuscado.

**MAS sí es detectado por Windows Defender**, siempre y por diseño — está advertido en la
propia web de massgrave.dev. El script lo avisa antes de lanzarlo y explica cómo apagar
temporalmente la protección en tiempo real y volver a encenderla al terminar.

## Capturas

En `capturas/` están todas las pantallas del programa:

- `pantalla-*.png` — limpias
- `figura-*.png` — con los recuadros y flechas rojas que usa el manual

Se regeneran con `python3 capturas/render.py`, que además comprueba dos cosas: que ninguna
caja del menú quede desalineada y que cada flecha del manual siga apuntando a un texto que
existe de verdad en la pantalla. `capturas/web.py` genera las dos pantallas de Windows.

## Aviso

Activar productos sin pagar la licencia va contra los términos de Microsoft. Este material
sirve para entender cómo funciona el mecanismo en un entorno de laboratorio. Al terminar la
práctica, restaure el snapshot de la máquina virtual.
