# =====================================================================
#  INSTITUTO SUPERIOR TECNOLOGICO POLICIA NACIONAL
#  Tecnologia Superior Universitaria en Prevencion del Delito
#  y Seguridad Ciudadana
#
#  Asignatura : Competencias Digitales      Unidad 1 de 3
#  Docente    : Mgtr. Maria del Carmen Salazar Torres
#  Seccion    : C
#
#  Instalador de Office para Windows 10 y 11.
#  Descarga TODO desde los servidores de Microsoft.
#  Material educativo para practicar en laboratorio.
# =====================================================================

$ErrorActionPreference = 'Stop'
$ProgressPreference    = 'SilentlyContinue'
try { [Console]::OutputEncoding = [Text.Encoding]::UTF8 } catch {}
try { $Host.UI.RawUI.WindowTitle = 'ISUPOL  ·  Instalador de Office' } catch {}

$MAS     = 'https://get.activated.win'
$TRABAJO = Join-Path $env:TEMP 'ISUPOL-Office'
$ANCHO   = 66

# Solo Word, Excel y PowerPoint. Para agregar Outlook, bórralo de la lista.
$EXCLUIR = 'Access','Groove','Lync','OneDrive','OneNote','Outlook',
           'OutlookForWindows','Publisher','Teams'

$CATALOGO = [ordered]@{
  '1' = @{ Nombre='Office 2016 Professional Plus'      ; Peso='2.5 GB'; Apps='Suite completa'
           Modo='C2R'; Id='ProPlusRetail' }
  '2' = @{ Nombre='Office 2019 Professional Plus'      ; Peso='1.8 GB'; Apps='Word Excel PPT'
           Modo='ODT'; Id='ProPlus2019Volume'; Canal='PerpetualVL2019' }
  '3' = @{ Nombre='Office LTSC 2021 Professional Plus' ; Peso='1.9 GB'; Apps='Word Excel PPT'
           Modo='ODT'; Id='ProPlus2021Volume'; Canal='PerpetualVL2021' }
  '4' = @{ Nombre='Office LTSC 2024 Professional Plus' ; Peso='2.1 GB'; Apps='Word Excel PPT'
           Modo='ODT'; Id='ProPlus2024Volume'; Canal='PerpetualVL2024' }
}

# ================================================================ dibujo
function Lin($car, $izq, $der, $color='DarkCyan') {
  Write-Host ('  ' + $izq + ($car * ($ANCHO + 2)) + $der) -ForegroundColor $color
}
function Fila($texto, $color='White', $borde='DarkCyan', $v='│') {
  Write-Host ('  ' + $v + ' ') -NoNewline -ForegroundColor $borde
  Write-Host $texto.PadRight($ANCHO) -NoNewline -ForegroundColor $color
  Write-Host (' ' + $v) -ForegroundColor $borde
}
function Centro($texto, $color='White', $borde='DarkCyan', $v='│') {
  $pad = [int](($ANCHO - $texto.Length) / 2)
  Fila ((' ' * [Math]::Max(0,$pad)) + $texto) $color $borde $v
}
function Dato($etiqueta, $valor, $color='White', $v='│') {
  Write-Host ('  ' + $v + ' ') -NoNewline -ForegroundColor DarkCyan
  Write-Host $etiqueta.PadRight(16) -NoNewline -ForegroundColor Gray
  Write-Host $valor.PadRight($ANCHO - 16) -NoNewline -ForegroundColor $color
  Write-Host (' ' + $v) -ForegroundColor DarkCyan
}
function Titulo($texto) {
  Write-Host ''
  Write-Host "   $texto" -ForegroundColor White
  Write-Host ('   ' + ('─' * $texto.Length)) -ForegroundColor DarkCyan
}

function Portada {
  Clear-Host
  Write-Host ''
  Lin '═' '╔' '╗'
  Centro 'INSTITUTO SUPERIOR TECNOLÓGICO' 'Cyan' 'DarkCyan' '║'
  Centro 'POLICÍA NACIONAL' 'Cyan' 'DarkCyan' '║'
  Centro 'Prevención del Delito y Seguridad Ciudadana' 'DarkGray' 'DarkCyan' '║'
  Lin '─' '╟' '╢'
  Dato '  Asignatura' 'Competencias Digitales          Unidad 1 de 3' 'White' '║'
  Dato '  Docente' 'Mgtr. María del Carmen Salazar Torres' 'White' '║'
  Dato '  Sección' 'C' 'White' '║'
  Lin '─' '╟' '╢'
  Centro 'INSTALADOR DE OFFICE' 'Yellow' 'DarkCyan' '║'
  Centro 'Descarga directa desde los servidores de Microsoft' 'DarkGray' 'DarkCyan' '║'
  Lin '═' '╚' '╝'
}

function Aviso($titulo, $lineas, $color='Yellow') {
  Write-Host ''
  Lin '═' '╔' '╗' $color
  Fila ('  (!)  ' + $titulo) $color $color '║'
  Lin '─' '╟' '╢' $color
  foreach ($l in $lineas) { Fila ('       ' + $l) 'White' $color '║' }
  Lin '═' '╚' '╝' $color
  Write-Host ''
}

function Exito($titulo, $lineas) {
  Write-Host ''
  Lin '═' '╔' '╗' 'Green'
  Centro $titulo 'Green' 'Green' '║'
  Lin '─' '╟' '╢' 'Green'
  foreach ($l in $lineas) { Fila ('       ' + $l) 'White' 'Green' '║' }
  Lin '═' '╚' '╝' 'Green'
  Write-Host ''
}

function Barra([double]$frac, $texto) {
  $n     = 38
  $lleno = [int]($frac * $n)
  $pct   = '{0,3:0}' -f ($frac * 100)
  Write-Host "`r   " -NoNewline
  Write-Host '[' -NoNewline -ForegroundColor DarkGray
  Write-Host ('█' * $lleno) -NoNewline -ForegroundColor Green
  Write-Host ('░' * ($n - $lleno)) -NoNewline -ForegroundColor DarkGray
  Write-Host ']' -NoNewline -ForegroundColor DarkGray
  Write-Host " $pct%  " -NoNewline -ForegroundColor Cyan
  Write-Host $texto.PadRight(24) -NoNewline -ForegroundColor Gray
}

function Paso($n, $de, $texto) {
  Write-Host ''
  Write-Host "   [$n/$de] " -NoNewline -ForegroundColor Yellow
  Write-Host $texto -ForegroundColor White
}

function Preguntar($pregunta, $texto1, $texto2, $color1='Green', $color2='Red') {
  Write-Host ''
  Write-Host "   $pregunta" -ForegroundColor White
  Write-Host '      1  ' -NoNewline -ForegroundColor $color1
  Write-Host $texto1 -ForegroundColor White
  Write-Host '      2  ' -NoNewline -ForegroundColor $color2
  Write-Host $texto2 -ForegroundColor White
  Write-Host ''
  (Read-Host '   Escribe 1 o 2 y pulsa Enter').Trim()
}

function Pausa($texto = 'Presiona cualquier tecla para volver al menú...') {
  Write-Host ''
  Write-Host "   $texto" -ForegroundColor Green
  try { $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown') } catch { Read-Host }
}

# ============================================================== utilidad
function Es-Admin {
  $id = [Security.Principal.WindowsIdentity]::GetCurrent()
  (New-Object Security.Principal.WindowsPrincipal $id).IsInRole(
    [Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Hay-Internet {
  try {
    $r = [Net.HttpWebRequest]::Create('https://officecdn.microsoft.com/pr/wsus/setup.exe')
    $r.Method = 'HEAD'; $r.Timeout = 8000
    $r.GetResponse().Close(); $true
  } catch { $false }
}

function Descargar($url, $destino, $etiqueta) {
  $req = [Net.HttpWebRequest]::Create($url)
  $req.Timeout = 30000
  $res   = $req.GetResponse()
  $total = $res.ContentLength
  $ent   = $res.GetResponseStream()
  $sal   = [IO.File]::Create($destino)
  $buf   = New-Object byte[] 65536
  $hecho = 0; $ultimo = -1
  try {
    while (($n = $ent.Read($buf, 0, $buf.Length)) -gt 0) {
      $sal.Write($buf, 0, $n)
      $hecho += $n
      if ($total -gt 0) {
        $pct = [int](100 * $hecho / $total)
        if ($pct -ne $ultimo) {          # repintar solo al cambiar de %
          $ultimo = $pct
          Barra ($hecho / $total) ('{0:N1} / {1:N1} MB' -f ($hecho/1MB), ($total/1MB))
        }
      }
    }
  } finally { $sal.Close(); $ent.Close(); $res.Close() }
  Barra 1 ('{0:N1} MB  ✓ {1}' -f ($hecho/1MB), $etiqueta)
  Write-Host ''
}

function Esperar($proc, $mensaje) {
  $marcos = '⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏'
  $i = 0; $t0 = Get-Date
  while (-not $proc.HasExited) {
    $t = (Get-Date) - $t0
    Write-Host ("`r   {0}  {1}  ·  transcurrido {2:mm\:ss}   " -f `
                $marcos[$i % 10], $mensaje, $t) -NoNewline -ForegroundColor Cyan
    Start-Sleep -Milliseconds 200
    $i++
  }
  Write-Host ("`r   ✓  {0}{1}" -f $mensaje, (' ' * 30)) -ForegroundColor Green
}

function Office-Instalado {
  Get-ChildItem "$env:ProgramFiles\Microsoft Office\root\Office16\WINWORD.EXE",
                "${env:ProgramFiles(x86)}\Microsoft Office\root\Office16\WINWORD.EXE" `
                -EA SilentlyContinue | Select-Object -First 1
}

# =========================================================== operaciones
function Nueva-Config($cuerpo) {
  $ruta = Join-Path $TRABAJO 'configuration.xml'
  [IO.File]::WriteAllText($ruta, $cuerpo, [Text.UTF8Encoding]::new($false))
  $ruta
}

function Xml-Instalar($prod, $bits, $idioma) {
  $apps = ($EXCLUIR | ForEach-Object { "      <ExcludeApp ID=`"$_`" />" }) -join "`r`n"
  @"
<Configuration>
  <Add OfficeClientEdition="$bits" Channel="$($prod.Canal)">
    <Product ID="$($prod.Id)">
      <Language ID="$idioma" />
$apps
    </Product>
  </Add>
  <Property Name="AUTOACTIVATE" Value="0" />
  <Property Name="FORCEAPPSHUTDOWN" Value="TRUE" />
  <Display Level="Full" AcceptEULA="TRUE" />
</Configuration>
"@
}

function Bajar-Setup {
  $setup = Join-Path $TRABAJO 'setup.exe'
  Descargar 'https://officecdn.microsoft.com/pr/wsus/setup.exe' $setup 'descargado'
  $setup
}

function Instalar-ODT($prod, $bits, $idioma) {
  Paso 1 3 'Descargando el instalador oficial de Microsoft'
  $setup = Bajar-Setup

  Paso 2 3 'Preparando la configuración de la instalación'
  $cfg = Nueva-Config (Xml-Instalar $prod $bits $idioma)
  Write-Host '   ✓  configuration.xml listo' -ForegroundColor Green

  Paso 3 3 'Instalando Office (se abrirá la ventana azul de Microsoft)'
  Write-Host ''
  $p = Start-Process $setup -ArgumentList "/configure `"$cfg`"" -PassThru
  Esperar $p 'Descargando e instalando Office'
  $p.ExitCode
}

function Instalar-C2R($prod, $bits, $idioma) {
  # Office 2016 no existe en el ODT moderno: se baja por c2rsetup.
  # Por esa vía Microsoft no permite excluir aplicaciones.
  $exe = Join-Path $TRABAJO 'OfficeSetup.exe'
  $url = 'https://c2rsetup.officeapps.live.com/c2r/download.aspx' +
         "?ProductreleaseID=$($prod.Id)&platform=x$bits&language=$idioma&version=O16GA"

  Paso 1 2 'Descargando el instalador oficial de Microsoft'
  Descargar $url $exe 'descargado'

  Paso 2 2 'Instalando Office 2016 (se abrirá la ventana de Microsoft)'
  Write-Host ''
  $p = Start-Process $exe -PassThru
  Esperar $p 'Descargando e instalando Office 2016'
  $p.ExitCode
}

function Accion-Instalar($op, $bits) {
  $prod   = $CATALOGO[$op]
  $idioma = 'es-es'

  Titulo 'Resumen de lo que se va a instalar'
  Lin '─' '┌' '┐'
  Dato '  Versión'      $prod.Nombre 'Cyan'
  Dato '  Aplicaciones' $prod.Apps
  Dato '  Idioma'       'Español (es-es)'
  Dato '  Arquitectura' "$bits bits"
  Dato '  Descarga'     "aproximadamente $($prod.Peso)"
  Lin '─' '└' '┘'

  Aviso 'NO CIERRES ESTA VENTANA' @(
    'La descarga y la instalación tardan entre 10 y 30',
    'minutos según tu internet.',
    '',
    'Cierra Word, Excel y PowerPoint antes de continuar.',
    'El script te avisará en verde cuando puedas cerrar.'
  )

  if ((Preguntar '¿Quieres instalarlo ahora?' `
                 'Sí, empezar la instalación' `
                 'No, volver al menú') -ne '1') {
    Write-Host ''
    Write-Host '   Cancelado. No se cambió nada en el equipo.' -ForegroundColor Gray
    Pausa; return
  }

  if (-not (Hay-Internet)) {
    Aviso 'SIN CONEXIÓN A INTERNET' @(
      'No se llega a los servidores de Microsoft.',
      'Revisa el cable o el WiFi y vuelve a intentarlo.'
    ) 'Red'
    Pausa; return
  }

  New-Item -ItemType Directory -Force -Path $TRABAJO | Out-Null

  try {
    $rc = if ($prod.Modo -eq 'ODT') { Instalar-ODT $prod $bits $idioma }
          else                      { Instalar-C2R $prod $bits $idioma }
  } catch {
    Aviso 'FALLÓ LA DESCARGA O LA INSTALACIÓN' @(
      $_.Exception.Message, '',
      'Revisa tu conexión y vuelve a intentarlo.'
    ) 'Red'
    Pausa; return
  }

  if (Office-Instalado) {
    Exito 'OFFICE INSTALADO CORRECTAMENTE' @(
      $prod.Nombre,
      '',
      'Ahora elige la opción 5 del menú para activarlo.'
    )
  } else {
    Aviso 'NO SE ENCONTRÓ WORD AL TERMINAR' @(
      "El instalador devolvió el código $rc.",
      'Busca los archivos .log dentro de la carpeta %temp%.'
    ) 'Red'
  }
  Pausa
}

function Accion-Activar {
  Titulo 'Activar Office con MAS'
  if (-not (Office-Instalado)) {
    Aviso 'NO HAY OFFICE INSTALADO' @(
      'No se encontró Word en este equipo.',
      'Instala primero con las opciones 1 a 4 del menú.'
    ) 'Red'
    Pausa; return
  }
  Aviso 'ANTES DE ACTIVAR' @(
    'Windows Defender detecta a MAS como herramienta de',
    'activación y puede bloquearlo. Es un falso positivo',
    'conocido, avisado en la propia web massgrave.dev.',
    '',
    'Si te lo bloquea: Seguridad de Windows → Protección',
    'antivirus → Administrar la configuración → apaga la',
    'Protección en tiempo real, activa Office, y vuelve',
    'a encenderla al terminar.'
  ) 'DarkYellow'
  Write-Host '   Se abrirá el menú de MAS. Dentro de él:' -ForegroundColor White
  Write-Host '      2 = activar Office      5 = ver estado      0 = salir de MAS' -ForegroundColor Gray
  if ((Preguntar '¿Abrir MAS ahora?' `
                 'Sí, abrir MAS' `
                 'No, volver al menú') -ne '1') { Pausa; return }
  Write-Host ''
  try { Invoke-Expression (Invoke-RestMethod $MAS) }
  catch {
    Aviso 'NO SE PUDO ABRIR MAS' @(
      $_.Exception.Message, '',
      'Puede ser el antivirus o la conexión.',
      "También puedes escribir a mano:  irm $MAS | iex"
    ) 'Red'
  }
  Pausa
}

function Accion-Ver {
  Titulo 'Office instalado en este equipo'
  $k = 'HKLM:\SOFTWARE\Microsoft\Office\ClickToRun\Configuration'
  if (-not (Test-Path $k)) {
    Aviso 'NO HAY OFFICE INSTALADO' @(
      'No se encontró ninguna instalación de Office.',
      'Usa las opciones 1 a 4 del menú para instalarlo.'
    ) 'DarkYellow'
    Pausa; return
  }
  $c = Get-ItemProperty $k
  Lin '─' '┌' '┐'
  Dato '  Producto'     ("$($c.ProductReleaseIds)")             'Cyan'
  Dato '  Versión'      ("$($c.VersionToReport)")
  Dato '  Idioma'       ("$($c.ClientCulture)")
  Dato '  Arquitectura' ("$($c.Platform)")
  Lin '─' '└' '┘'

  Write-Host ''
  Write-Host '   Estado de la licencia:' -ForegroundColor White
  $ospp = "$env:ProgramFiles\Microsoft Office\Office16\ospp.vbs",
          "${env:ProgramFiles(x86)}\Microsoft Office\Office16\ospp.vbs" |
          Where-Object { Test-Path $_ } | Select-Object -First 1
  if ($ospp) {
    cscript //nologo $ospp /dstatus 2>$null |
      Select-String 'LICENSE STATUS|LICENSE NAME|remaining' |
      ForEach-Object { Write-Host ('     ' + $_.Line.Trim()) -ForegroundColor Gray }
  } else {
    Write-Host '     No se pudo consultar (usa la opción 5 → MAS → 5).' -ForegroundColor DarkGray
  }
  Pausa
}

function Accion-Desinstalar {
  Titulo 'Desinstalar Office de este equipo'
  if (-not (Office-Instalado)) {
    Aviso 'NO HAY NADA QUE DESINSTALAR' @('No se encontró Office en este equipo.') 'DarkYellow'
    Pausa; return
  }
  Aviso 'ESTO BORRA OFFICE DEL EQUIPO' @(
    'Se quitarán Word, Excel, PowerPoint y lo demás.',
    'Tus documentos NO se borran, solo los programas.',
    '',
    'Fíjate bien: aquí el 1 es CANCELAR.'
  ) 'Red'
  # ponytail: el 1 cancela a propósito, para que pulsarlo por inercia no borre nada
  if ((Preguntar '¿Seguro que quieres borrar Office?' `
                 'No, cancelar y volver al menú' `
                 'Sí, borrar Office de este equipo' `
                 'Green' 'Red') -ne '2') {
    Write-Host ''
    Write-Host '   Cancelado. No se tocó nada.' -ForegroundColor Gray
    Pausa; return
  }
  New-Item -ItemType Directory -Force -Path $TRABAJO | Out-Null
  Paso 1 2 'Descargando la herramienta de Microsoft'
  $setup = Bajar-Setup
  Paso 2 2 'Desinstalando Office'
  $cfg = Nueva-Config @"
<Configuration>
  <Remove All="TRUE" />
  <Property Name="FORCEAPPSHUTDOWN" Value="TRUE" />
  <Display Level="Full" AcceptEULA="TRUE" />
</Configuration>
"@
  Write-Host ''
  $p = Start-Process $setup -ArgumentList "/configure `"$cfg`"" -PassThru
  Esperar $p 'Desinstalando Office'
  if (Office-Instalado) {
    Aviso 'OFFICE SIGUE INSTALADO' @('La desinstalación no terminó bien.') 'Red'
  } else {
    Exito 'OFFICE DESINSTALADO' @('El equipo quedó limpio.')
  }
  Pausa
}

function Accion-Ayuda {
  Titulo 'Qué hace este programa'
  Lin '─' '┌' '┐'
  Fila '  Este instalador descarga Office directamente de los'
  Fila '  servidores de Microsoft. No usa páginas de terceros'
  Fila '  ni archivos de dudosa procedencia.'
  Fila ''
  Fila '  Opciones 1 a 4   Instalan la versión que elijas. Solo'
  Fila '                   Word, Excel y PowerPoint (menos la'
  Fila '                   2016, que instala la suite completa'
  Fila '                   porque Microsoft no deja elegir).'
  Fila ''
  Fila '  Opción 5         Abre MAS (massgrave.dev) para activar.'
  Fila '  Opción 6         Muestra qué Office tienes y su licencia.'
  Fila '  Opción 7         Borra Office del equipo.'
  Fila ''
  Fila '  Es material de laboratorio para la asignatura.' 'DarkGray'
  Fila '  Al terminar la práctica, restaura el snapshot.' 'DarkGray'
  Lin '─' '└' '┘'
  Pausa
}

# ================================================================== main
Portada

$build = [Environment]::OSVersion.Version.Build
$admin = Es-Admin
$bits  = if ([Environment]::Is64BitOperatingSystem) { '64' } else { '32' }
$disco = $env:SystemDrive
try { $libre = [math]::Round((Get-PSDrive $disco.TrimEnd(':')).Free / 1GB, 1) } catch { $libre = 0 }
$so    = if ($build -ge 22000) { 'Windows 11' } elseif ($build -ge 10240) { 'Windows 10' } else { 'no compatible' }
try { $rtp = (Get-MpComputerStatus).RealTimeProtectionEnabled } catch { $rtp = $null }

Titulo 'Revisión del equipo'
Lin '─' '┌' '┐'
Dato '  Sistema'      "$so  (build $build)" $(if ($build -ge 10240) {'Green'} else {'Red'})
Dato '  Arquitectura' "$bits bits"
Dato '  Permisos'     $(if ($admin) {'Administrador'} else {'SIN permisos de administrador'}) $(if ($admin) {'Green'} else {'Red'})
Dato "  Espacio en $disco" "$libre GB libres" $(if ($libre -ge 5) {'Green'} else {'Red'})
Dato '  Defender'     $(if ($rtp -eq $true) {'Protección en tiempo real activa'} elseif ($rtp -eq $false) {'Protección en tiempo real apagada'} else {'no se pudo consultar'}) 'Gray'
Dato '  Office'       $(if (Office-Instalado) {'ya instalado'} else {'no instalado'}) 'Gray'
Lin '─' '└' '┘'

if ($build -lt 10240) {
  Aviso 'ESTE EQUIPO NO ES COMPATIBLE' @(
    'El script necesita Windows 10 o Windows 11.',
    'Office 2019, 2021 y 2024 no se instalan en versiones',
    'anteriores de Windows.'
  ) 'Red'
  Pausa 'Presiona cualquier tecla para cerrar...'; return
}

if (-not $admin) {
  Aviso 'FALTAN PERMISOS DE ADMINISTRADOR' @(
    'Cierra esta ventana.',
    'Pulsa la tecla Windows, escribe  PowerShell,',
    'y elige  "Ejecutar como administrador".',
    'Después vuelve a abrir este instalador.'
  ) 'Red'
  Pausa 'Presiona cualquier tecla para cerrar...'; return
}

if ($libre -lt 5) {
  Aviso 'ESPACIO INSUFICIENTE EN EL DISCO' @(
    "Tienes $libre GB libres y hacen falta al menos 5 GB.",
    'Libera espacio y vuelve a ejecutar el instalador.'
  ) 'Red'
  Pausa 'Presiona cualquier tecla para cerrar...'; return
}

# --- bucle del menú -----------------------------------------------------
while ($true) {
  Portada
  Write-Host ''
  Write-Host '   INSTALAR OFFICE' -ForegroundColor White
  Write-Host '  ┌─────┬─────────────────────────────────────┬──────────┬────────────────┐' -ForegroundColor DarkCyan
  Write-Host '  │  #  │ Versión                             │  Descarga│ Aplicaciones   │' -ForegroundColor Gray
  Write-Host '  ├─────┼─────────────────────────────────────┼──────────┼────────────────┤' -ForegroundColor DarkCyan
  foreach ($k in $CATALOGO.Keys) {
    $p = $CATALOGO[$k]
    Write-Host '  │  ' -NoNewline -ForegroundColor DarkCyan
    Write-Host $k -NoNewline -ForegroundColor Green
    Write-Host '  │ ' -NoNewline -ForegroundColor DarkCyan
    Write-Host $p.Nombre.PadRight(36) -NoNewline -ForegroundColor White
    Write-Host '│ ' -NoNewline -ForegroundColor DarkCyan
    Write-Host ('≈ ' + $p.Peso).PadRight(9) -NoNewline -ForegroundColor Yellow
    Write-Host '│ ' -NoNewline -ForegroundColor DarkCyan
    Write-Host $p.Apps.PadRight(15) -NoNewline -ForegroundColor Gray
    Write-Host '│' -ForegroundColor DarkCyan
  }
  Write-Host '  └─────┴─────────────────────────────────────┴──────────┴────────────────┘' -ForegroundColor DarkCyan

  Write-Host ''
  Write-Host '   OTRAS OPCIONES' -ForegroundColor White
  Write-Host '  ┌─────┬─────────────────────────────────────────────────────────────────┐' -ForegroundColor DarkCyan
  $otras = @(
    @('5','Activar Office con MAS  (massgrave.dev)','Cyan'),
    @('6','Ver qué Office tengo y si está activado','Cyan'),
    @('7','Desinstalar Office de este equipo','DarkYellow'),
    @('8','Ayuda: qué hace cada opción','Gray'),
    @('9','Salir del programa','Red')
  )
  foreach ($o in $otras) {
    Write-Host '  │  ' -NoNewline -ForegroundColor DarkCyan
    Write-Host $o[0] -NoNewline -ForegroundColor $o[2]
    Write-Host '  │ ' -NoNewline -ForegroundColor DarkCyan
    Write-Host $o[1].PadRight(64) -NoNewline -ForegroundColor White
    Write-Host '│' -ForegroundColor DarkCyan
  }
  Write-Host '  └─────┴─────────────────────────────────────────────────────────────────┘' -ForegroundColor DarkCyan
  Write-Host ''

  $op = (Read-Host '   Escribe el número de la opción y pulsa Enter').Trim()

  switch ($op) {
    { $CATALOGO.Contains($_) } { Accion-Instalar $op $bits }
    '5' { Accion-Activar }
    '6' { Accion-Ver }
    '7' { Accion-Desinstalar }
    '8' { Accion-Ayuda }
    '9' {
      Portada
      Write-Host ''
      Write-Host '   Recuerda: es una práctica de laboratorio.' -ForegroundColor DarkGray
      Write-Host '   Al terminar, restaura el snapshot de la máquina virtual.' -ForegroundColor DarkGray
      Pausa 'Ya puedes cerrar. Presiona cualquier tecla...'
      return
    }
    default {
      Aviso 'ESA OPCIÓN NO EXISTE' @(
        "Escribiste `"$op`".",
        'Los números válidos son del 1 al 9.'
      ) 'Red'
      Pausa
    }
  }
}
