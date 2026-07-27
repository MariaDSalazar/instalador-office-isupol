#!/usr/bin/env python3
"""Genera MANUAL-Instalar-Office.html completo (CSS del archivo actual + cuerpo nuevo).
Todo el texto va en tratamiento de usted."""
import pathlib, re

P = pathlib.Path('/mnt/disco1tb/diego/office_script/MANUAL-Instalar-Office.html')
css = P.read_text(encoding='utf-8').split('</head>')[0] + '</head>\n'

AZ = '#2166ac'
def svg(c, w=24):
    return (f'<svg class="ico" width="{w}" height="{w}" viewBox="0 0 24 24" '
            f'xmlns="http://www.w3.org/2000/svg">{c}</svg>')

RATON = (f'<rect x="7" y="2" width="10" height="20" rx="5" fill="none" stroke="{AZ}" '
         f'stroke-width="1.7"/><path d="M12 2.5v7M7.4 9.5h9.2" stroke="{AZ}" stroke-width="1.4"/>')
I = {
 'clic':   svg(RATON + f'<path d="M8 4.5a4.4 4.4 0 0 1 3.4-2.3V9H7.6z" fill="{AZ}"/>'),
 'doble':  svg(RATON + f'<path d="M8 4.5a4.4 4.4 0 0 1 3.4-2.3V9H7.6z" fill="{AZ}"/>'
                     + f'<path d="M18.5 4.5l2 1M18.5 7l2 .4" stroke="{AZ}" stroke-width="1.4" stroke-linecap="round"/>'),
 'der':    svg(RATON + f'<path d="M12.6 2.2A4.4 4.4 0 0 1 16 4.5V9h-3.4z" fill="{AZ}"/>'),
 'win':    svg(f'<rect x="2.5" y="3" width="8.4" height="8" fill="{AZ}"/>'
               f'<rect x="13.1" y="3" width="8.4" height="8" fill="{AZ}"/>'
               f'<rect x="2.5" y="13" width="8.4" height="8" fill="{AZ}"/>'
               f'<rect x="13.1" y="13" width="8.4" height="8" fill="{AZ}"/>'),
 'tareas': svg(f'<rect x="1.5" y="14" width="21" height="7" rx="1.5" fill="none" stroke="{AZ}" stroke-width="1.7"/>'
               f'<rect x="4" y="16.2" width="3.4" height="3.4" rx=".7" fill="{AZ}"/>'
               f'<rect x="9" y="16.2" width="3.4" height="3.4" rx=".7" fill="{AZ}"/>'
               f'<rect x="14" y="16.2" width="3.4" height="3.4" rx=".7" fill="{AZ}"/>'),
 'ps':     svg('<rect x="1.5" y="3.5" width="21" height="17" rx="2" fill="#012456"/>'
               '<path d="M6 8.5l4 3.4-4 3.4M11.5 16h6" stroke="#fff" stroke-width="1.8" '
               'fill="none" stroke-linecap="round" stroke-linejoin="round"/>'),
 'cmd':    svg(f'<rect x="1.5" y="4.5" width="21" height="15" rx="2" fill="none" stroke="{AZ}" stroke-width="1.7"/>'
               f'<path d="M5.5 9h13M5.5 12h9M5.5 15h6" stroke="{AZ}" stroke-width="1.5" stroke-linecap="round"/>'),
 'admin':  svg(f'<path d="M12 2.2l8 3v6c0 5-3.4 9.2-8 10.6C7.4 20.4 4 16.2 4 11.2v-6z" '
               f'fill="none" stroke="{AZ}" stroke-width="1.7"/>'
               f'<path d="M8.4 11.8l2.5 2.6 4.7-5" stroke="{AZ}" stroke-width="1.9" '
               'fill="none" stroke-linecap="round" stroke-linejoin="round"/>'),
 'copiar': svg(f'<rect x="8" y="8" width="13" height="13" rx="2" fill="none" stroke="{AZ}" stroke-width="1.7"/>'
               f'<path d="M16 5.5V4a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v11a1 1 0 0 0 1 1h1.5" '
               f'fill="none" stroke="{AZ}" stroke-width="1.7"/>'),
 'llave':  svg(f'<circle cx="7.5" cy="12" r="4.2" fill="none" stroke="{AZ}" stroke-width="1.8"/>'
               f'<path d="M11.7 12H21m-3 0v3.4m-3-3.4v2.4" stroke="{AZ}" stroke-width="1.8" stroke-linecap="round"/>'),
 'consola':svg('<rect x="1.5" y="3.5" width="21" height="17" rx="2" fill="#0C0C0C" stroke="#555" stroke-width="1"/>'
               '<path d="M5 9l3.4 2.8L5 14.6" stroke="#16C60C" stroke-width="1.7" fill="none" '
               'stroke-linecap="round" stroke-linejoin="round"/>'
               '<path d="M10 15.4h7" stroke="#16C60C" stroke-width="1.7" stroke-linecap="round"/>'),
 'enter':  svg(f'<path d="M20 5v7H6" fill="none" stroke="{AZ}" stroke-width="1.9" stroke-linecap="round"/>'
               f'<path d="M9.5 8.5L6 12l3.5 3.5" fill="none" stroke="{AZ}" stroke-width="1.9" '
               'stroke-linecap="round" stroke-linejoin="round"/>'),
}
POWER = ('<svg class="ico" width="17" height="17" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
         '<path d="M12 3.2v8.4" stroke="#333" stroke-width="2.3" stroke-linecap="round"/>'
         '<path d="M7 6.6a7.4 7.4 0 1 0 10 0" fill="none" stroke="#333" stroke-width="2.3" '
         'stroke-linecap="round"/></svg>')

GLOS = [
 ('clic',   'Clic', 'Presionar una vez el botón izquierdo del ratón (el mouse).'),
 ('doble',  'Doble clic', 'Presionar ese mismo botón dos veces seguidas y rápido.'),
 ('der',    'Clic derecho', 'Presionar el botón derecho del ratón. Casi siempre abre un menucito con opciones.'),
 ('win',    'Menú Inicio', 'El menú que se abre al presionar la tecla <span class="tecla">Windows</span> (abajo a la izquierda).'),
 ('tareas', 'Barra de tareas', 'La barra de iconos que está abajo del todo de la pantalla.'),
 ('ps',     'PowerShell', 'Un programa de Windows, con fondo azul oscuro, donde todo se hace escribiendo. No tiene botones.'),
 ('cmd',    'Comando', 'Una línea de texto que se le da a PowerShell para que haga algo. En este manual se copia y se pega; no hace falta escribirla a mano.'),
 ('admin',  'Administrador', 'Permiso especial que Windows exige para instalar programas. Sin él, la instalación no puede ni empezar.'),
 ('copiar', 'Copiar y pegar', 'Copiar guarda un texto en la memoria (<span class="tecla">Ctrl</span>+<span class="tecla">C</span>); pegar lo suelta donde se necesite (<span class="tecla">Ctrl</span>+<span class="tecla">V</span>).'),
 ('enter',  'Tecla Enter', 'La tecla grande con la flecha doblada. Confirma lo que se acaba de escribir.'),
 ('consola','Ventana de la consola', 'La ventana sin botones donde el instalador muestra su menú. Todo se elige escribiendo un número.'),
 ('llave',  'Activar', 'Darle a Office una licencia para que funcione sin límites ni avisos.'),
]
glos = '<table class="glos2">\n' + ''.join(
    f'  <tr><td class="ic">{I[k]}</td><td><b>{t}:</b> {d}</td></tr>\n' for k, t, d in GLOS) + '</table>'

PROMPT = 'PS C:' + chr(92) + 'Windows' + chr(92) + 'system32&gt;'
PROMPT2 = 'PS C:' + chr(92) + '...'
CMD = ('irm https://raw.githubusercontent.com/MariaDSalazar/'
       'instalador-office-isupol/main/office-isupol.ps1 | iex')

def fig(archivo, alt, num, pie):
    return (f'<figure>\n  <img src="capturas/{archivo}" alt="{alt}">\n'
            f'  <figcaption><b>Figura {num}.</b> {pie}</figcaption>\n</figure>')

def err(mensaje, causa, solucion):
    return (f'<h5>«{mensaje[:70]}…»</h5>\n' if len(mensaje) > 70 else f'<h5>«{mensaje}»</h5>\n') + \
           (f'<div class="errbox">{mensaje}</div>\n'
            f'<p class="chico"><b>Por qué pasa:</b> {causa}<br>'
            f'<b>Cómo se soluciona:</b> {solucion}</p>')

cuerpo = f"""<body>

<div class="inst">
  <h1>INSTITUTO SUPERIOR TECNOLÓGICO POLICÍA NACIONAL</h1>
  <h2>Tecnología Superior Universitaria en Prevención del Delito y Seguridad Ciudadana</h2>
</div>

<div class="doctag">MANUAL DE USUARIO PASO A PASO (PARA PRINCIPIANTES)</div>
<div class="titulo">Instalar Office desde cero</div>
<div class="subtitulo">Unidad 1 · Instalación de software ofimático</div>

<table class="datos">
  <tr><td class="k">Asignatura:</td><td>Competencias Digitales</td>
      <td class="k">Docente:</td><td>Mgtr. María del Carmen Salazar Torres</td></tr>
  <tr><td class="k">Unidad:</td><td>1 de 3</td>
      <td class="k">Curso / Paralelo:</td><td>Sección C</td></tr>
  <tr><td class="k">Tipo de documento:</td><td colspan="3">Manual instructivo de uso.
      Material de apoyo para seguir paso a paso; no es una tarea evaluada ni se entrega.</td></tr>
</table>

<h3>1. Instrucciones</h3>
<p class="chico">Este manual está pensado para quien nunca ha instalado un programa. Se
parte desde encender la computadora y no se da nada por sabido. Cada captura lleva
<b style="color:#c0392b">flechas rojas</b> que señalan exactamente dónde mirar y qué
escribir. No hay nada que entregar ni que rellenar: es solo para seguirlo mientras se
instala. Conviene ir paso por paso, sin prisa: realizar una acción y recién pasar a la
siguiente. Las pruebas se realizan en el laboratorio, nunca en el equipo real; al terminar
se restaura el snapshot de la máquina virtual. Calcule entre 30 y 45 minutos.</p>

<div class="nota"><b>Cómo leer este manual.</b> Las teclas del teclado se escriben así:
<span class="tecla">Windows</span> <span class="tecla">Enter</span>. La flecha →
significa «y luego» (por ejemplo: haga clic → escriba → pulse Enter). Los números que hay
que escribir en el programa aparecen así: <span class="num">3</span>.</div>

<h3>2. Pequeño glosario (palabras que se van a usar)</h3>
{glos}

<h3>3. Historias de usuario (para qué sirve esto)</h3>
<ul class="chico">
  <li>Como estudiante que nunca ha instalado Office, quiero seguir pasos con imágenes,
      flechas y números para no perderme en ningún momento.</li>
  <li>Como usuario nuevo, quiero ver exactamente qué escribir y dónde, para no equivocarme
      ni borrar algo por error.</li>
  <li>Como principiante, quiero reconocer la señal de que salió bien para quedarme tranquilo.</li>
</ul>

<div class="alerta"><b>Antes de empezar.</b> Esto se realiza en la máquina virtual del
laboratorio, nunca en la computadora personal. Al terminar la práctica se restaura el
snapshot y el equipo queda como estaba.</div>

<h3 class="salto">4. Manual paso a paso</h3>

<h4 class="paso">Paso A. Encender la computadora y entrar a Windows</h4>
<ol class="pasos">
  <li>Presione el botón de encendido <b>una sola vez</b> y suéltelo.
      <span class="sub">En una computadora de escritorio está en la torre (la caja grande).
      En una laptop, arriba del teclado. Tiene dibujado este símbolo: {POWER}</span></li>
  <li>Espere sin tocar nada.
      <span class="sub">Se verán luces y quizá un logo. Puede tardar uno o dos minutos. Es normal.</span></li>
  <li>Aparece una pantalla con la hora (se llama pantalla de bloqueo). Presione cualquier
      tecla o haga clic para continuar.</li>
  <li>Escriba su contraseña o PIN y pulse <span class="tecla">Enter</span>.
      <span class="sub">Si el equipo no pide contraseña, entra directo.</span></li>
  <li>Ya está dentro cuando ve el fondo de pantalla con iconos y, abajo, la barra de tareas.</li>
</ol>

<h4 class="paso">Paso B. Abrir PowerShell como administrador</h4>
<p class="chico">Este es <b>el paso más importante de todo el manual</b>. Si PowerShell se
abre sin permisos de administrador, la instalación no podrá empezar.</p>
<ol class="pasos">
  <li>Presione la tecla <span class="tecla">Windows</span> {I['win']} del teclado
      (la que tiene la ventanita). Se abre el menú Inicio.</li>
  <li>Escriba <code>PowerShell</code>. <b>No pulse Enter todavía.</b>
      <span class="sub">Arriba aparecerá «Windows PowerShell» como mejor coincidencia.</span></li>
  <li>En el panel de la derecha, haga clic en <b>«Ejecutar como administrador»</b>.
      <span class="sub">Si no aparece ese panel, haga clic derecho sobre «Windows
      PowerShell» y elija esa misma opción del menú.</span></li>
  <li>Windows preguntará si permite cambios en el dispositivo. Haga clic en <b>Sí</b>.
      <span class="sub">Ese aviso es normal y sale siempre. Si se pulsa «No», la ventana
      se cierra y no ocurre nada.</span></li>
</ol>

{fig('figura-win1.png', 'Buscar PowerShell en el menú Inicio', 1,
     'El menú Inicio tras escribir «PowerShell». <b>Recuadro 1:</b> lo que se escribió. '
     '<b>Recuadro 2:</b> la opción que hay que elegir. Si se hace clic en «Abrir», el '
     'programa se abre sin permisos y el instalador no podrá continuar.')}

{fig('figura-win2.png', 'El aviso de permisos de Windows', 2,
     'Este aviso es normal y aparece siempre que un programa necesita permisos de '
     'administrador. La flecha señala el botón <b>Sí</b>, que es el que hay que pulsar.')}

{fig('figura-ps1.png', 'PowerShell recién abierta', 3,
     'La ventana de PowerShell recién abierta. En el título de arriba debe aparecer la '
     'palabra <b>«Administrador»</b>: eso confirma que tiene los permisos correctos. '
     'La flecha señala el punto donde se pegará el comando.')}

<div class="peligro"><b>Si el título no dice «Administrador»</b>, cierre la ventana y
vuelva a abrirla con la opción <b>Ejecutar como administrador</b>. Sin esos permisos, el
instalador se detendrá con un aviso en rojo.</div>

<h4 class="paso">Paso C. Copiar el comando y ejecutarlo</h4>
<p class="chico">El comando es la línea que aparece a continuación. <b>No hace falta
escribirla a mano:</b> se selecciona con el ratón y se copia.</p>

<div class="comando">{CMD}</div>

<ol class="pasos">
  <li>Seleccione la línea de arriba: haga clic al principio del texto y, sin soltar,
      arrastre hasta el final.</li>
  <li>Pulse <span class="tecla">Ctrl</span>+<span class="tecla">C</span> para copiarla.
      {I['copiar']}
      <span class="sub">No se verá ningún cambio en la pantalla. Es normal: el texto queda
      guardado en la memoria.</span></li>
  <li>Vaya a la ventana de PowerShell y haga <b>clic derecho una sola vez</b> dentro.
      El comando aparece solo.
      <span class="sub">También sirve <span class="tecla">Ctrl</span>+<span class="tecla">V</span>.
      En PowerShell el clic derecho pega directamente; es normal que no salga ningún menú.</span></li>
  <li>Compruebe que la línea esté completa y termine en <code>| iex</code>.</li>
  <li>Pulse <span class="tecla">Enter</span> {I['enter']} y espere unos segundos.</li>
</ol>

{fig('figura-ps2.png', 'El comando pegado en PowerShell', 4,
     'Así se ve el comando ya pegado, justo después de <code>' + PROMPT + '</code>. '
     'Es tan largo que la consola lo parte en dos líneas: eso es normal y no es un error. '
     'Solo falta pulsar <span class="tecla">Enter</span>.')}

<div class="nota"><b>Qué hace ese comando.</b> <code>irm</code> descarga el instalador y
<code>iex</code> lo pone en marcha. Es la misma forma de trabajar que usa massgrave.dev.
El archivo procede del repositorio de la asignatura y descarga Office únicamente de los
servidores de Microsoft.</div>

{fig('figura-01.png', 'Portada del instalador', 5,
     'Lo primero que aparece tras pulsar Enter. Si se ve el nombre del Instituto y el '
     'título «INSTALADOR DE OFFICE», el programa arrancó correctamente.')}

<div class="alerta"><b>¿Salió un error en rojo y no apareció el menú?</b> Es lo más común
y tiene arreglo. La <b>sección 5</b> de este manual recoge los errores más frecuentes con
su solución exacta.</div>

<h4 class="paso">Paso D. Leer la revisión del equipo</h4>
<p class="chico">Antes de descargar nada, el programa revisa la computadora.
<b>Todo lo que esté en verde está bien.</b> Si algo sale en rojo, el programa se detiene y
explica qué hacer.</p>

{fig('figura-02.png', 'Revisión del equipo', 6,
     'La tabla de revisión. Las flechas explican qué significa cada línea. La más '
     'importante es <b>Permisos</b>: debe decir «Administrador» y estar en verde.')}

<table class="tab">
  <tr><th style="width:22%">Línea</th><th>Qué significa</th><th style="width:26%">Debe decir</th></tr>
  <tr><td>Sistema</td><td>Qué versión de Windows tiene el equipo</td><td>Windows 10 o Windows 11</td></tr>
  <tr><td>Arquitectura</td><td>Si el Windows es de 32 o 64 bits. Se detecta solo</td><td>64 bits (lo normal)</td></tr>
  <tr><td>Permisos</td><td>Si el programa puede instalar</td><td><b>Administrador</b>, en verde</td></tr>
  <tr><td>Espacio en C:</td><td>Cuánto espacio libre queda en el disco</td><td>Al menos 5 GB</td></tr>
  <tr><td>Defender</td><td>Si el antivirus está encendido. Solo informativo</td><td>Cualquiera de las dos</td></tr>
  <tr><td>Office</td><td>Si ya hay un Office instalado</td><td>Cualquiera de las dos</td></tr>
</table>

<h4 class="paso">Paso E. Elegir qué Office se va a instalar</h4>
<p class="chico">Debajo de la revisión aparece el menú, dividido en dos tablas.
<b>Todo se elige escribiendo un número y pulsando <span class="tecla">Enter</span>.</b>
El ratón no sirve aquí.</p>

{fig('figura-03.png', 'Tabla de versiones', 7,
     'La primera tabla: las cuatro versiones disponibles. La primera columna es el número '
     'que se va a escribir. Si no se sabe cuál elegir, la flecha señala la <b>opción 3</b>.')}

<table class="tab">
  <tr><th style="width:9%">Número</th><th>Qué instala</th><th style="width:26%">Aplicaciones</th></tr>
  <tr><td><span class="num">1</span></td><td>Office 2016 Professional Plus</td><td>La suite completa</td></tr>
  <tr><td><span class="num">2</span></td><td>Office 2019 Professional Plus</td><td>Word, Excel, PowerPoint</td></tr>
  <tr><td><span class="num">3</span></td><td>Office LTSC 2021 Professional Plus</td><td>Word, Excel, PowerPoint</td></tr>
  <tr><td><span class="num">4</span></td><td>Office LTSC 2024 Professional Plus</td><td>Word, Excel, PowerPoint</td></tr>
</table>
<p class="chico" style="color:#555">La opción 1 instala además Access, Publisher y OneNote,
porque en esa versión Microsoft no permite elegir aplicaciones sueltas.</p>

{fig('figura-04.png', 'Otras opciones del menú', 8,
     'La segunda tabla: lo que <i>no</i> es instalar. Aquí está la opción <b>5</b> para '
     'activar, la <b>6</b> para comprobar y la <b>9</b> para salir. Conviene fijarse en la '
     'advertencia de la opción 7.')}

{fig('figura-05.png', 'Dónde escribir el número', 9,
     'La última línea de la pantalla es donde se escribe. La flecha señala el sitio exacto: '
     'se teclea el número y se pulsa <span class="tecla">Enter</span>.')}

<ol class="pasos">
  <li>Decida qué versión quiere con la tabla de arriba.
      <span class="sub">Si no lo tiene claro, elija la <span class="num">3</span>. Es la más
      usada y trae solo Word, Excel y PowerPoint.</span></li>
  <li>Escriba ese número con el teclado. Aparecerá al final de la línea, en amarillo.</li>
  <li>Pulse <span class="tecla">Enter</span>.</li>
</ol>

<div class="nota"><b>¿Se equivocó de tecla?</b> Si escribe una letra o un número que no
existe, el programa avisa en rojo y devuelve al menú. No ocurre nada malo y se puede
volver a intentar las veces que haga falta.</div>

<h4 class="paso">Paso F. Confirmar antes de instalar</h4>
<p class="chico">El programa nunca instala nada sin preguntar. Primero muestra un resumen
para comprobar que la elección fue la correcta.</p>

{fig('figura-06.png', 'Resumen de la instalación', 10,
     'El resumen. Las flechas señalan las tres cosas que hay que revisar: la versión, los '
     'programas que trae y cuánto se va a descargar.')}

{fig('figura-07.png', 'Aviso de no cerrar', 11,
     'El aviso amarillo. Conviene leerlo entero antes de seguir: hay que cerrar Word, Excel '
     'y PowerPoint si están abiertos.')}

{fig('figura-08.png', 'Confirmación 1 o 2', 12,
     'La confirmación. Aquí no se escribe «sí» ni «no»: se escribe <b>1</b> para instalar o '
     '<b>2</b> para volver al menú.')}

<ol class="pasos">
  <li>Cierre Word, Excel y PowerPoint si están abiertos.</li>
  <li>Lea el resumen y compruebe que sea la versión correcta.</li>
  <li>Escriba <span class="num">1</span> → <span class="tecla">Enter</span> para empezar.</li>
</ol>

<h4 class="paso">Paso G. Esperar sin cerrar la ventana</h4>

<div class="peligro"><b>No cierre la ventana de PowerShell.</b> La descarga y la instalación
tardan entre 10 y 30 minutos según la conexión. Si se cierra a la mitad, Office queda
instalado a medias y hay que empezar de nuevo. El programa avisará <b>en verde</b> cuando
se pueda cerrar.</div>

{fig('figura-09.png', 'Barra de descarga', 13,
     'La barra de descarga. Se llena sola de izquierda a derecha. Las flechas señalan el '
     'porcentaje (va de 0 a 100) y los megabytes que lleva descargados.')}

{fig('figura-10.png', 'Los tres pasos de la instalación', 14,
     'Los tres pasos. El más largo es el tercero. La flecha señala el reloj: <b>mientras '
     'ese número avance, todo va bien</b>, aunque la pantalla parezca detenida.')}

<div class="nota"><b>Se abrirá otra ventana azul de Microsoft</b> con su propia barra de
progreso. Es normal: es el instalador oficial haciendo su trabajo. Tampoco hay que cerrarla.</div>

{fig('figura-11.png', 'Office instalado correctamente', 15,
     '<b>La señal de que salió bien:</b> el cartel verde. Las flechas señalan la '
     'confirmación y el siguiente paso. Si aparece esto, Office ya está instalado.')}

<h4 class="paso">Paso H. Activar Office</h4>
<p class="chico">Office ya está instalado, pero le falta la licencia. Desde el menú, se
escribe <span class="num">5</span>.</p>

{fig('figura-12.png', 'Aviso sobre el antivirus', 16,
     'El aviso naranja sobre el antivirus. Las flechas señalan las dos partes importantes: '
     'que no se trata de un virus real, y los pasos para apagar la protección un rato si '
     'hiciera falta.')}

<div class="alerta"><b>Por qué se queja el antivirus.</b> Windows Defender marca
<i>todas</i> las herramientas de activación, aunque no sean dañinas. La propia página
massgrave.dev lo advierte. Si las bloquea: abra <b>Seguridad de Windows</b> →
<b>Protección antivirus y contra amenazas</b> → <b>Administrar la configuración</b> →
apague <b>Protección en tiempo real</b> → active Office →
<b>vuelva a encenderla al terminar</b>. No debe dejarse el antivirus apagado.</div>

{fig('figura-13.png', 'Números que se usan en MAS', 17,
     'Conviene no confundirse: hay dos menús distintos. La flecha de abajo es el <b>1</b> '
     'de <i>este</i> programa (abrir MAS). La de arriba es el <b>2</b> que se escribirá '
     '<i>dentro</i> de MAS, que es otro menú.')}

<ol class="pasos">
  <li>En el menú escriba <span class="num">5</span> → <span class="tecla">Enter</span>.</li>
  <li>Lea el aviso naranja del antivirus.</li>
  <li>Escriba <span class="num">1</span> → <span class="tecla">Enter</span> para abrir MAS.</li>
  <li>Se abre el menú de MAS, con opciones de colores.
      <span class="sub">Es otro programa distinto, con su propio menú.</span></li>
  <li>Con Office cerrado, escriba <span class="num">2</span> → <span class="tecla">Enter</span>.
      <span class="sub">El 2 de MAS corresponde a «Ohook — Office». El 1 sería Windows, que
      aquí no toca.</span></li>
  <li>Espere sin tocar nada hasta que aparezca una <b>línea en verde</b>.</li>
  <li>Escriba <span class="num">0</span> → <span class="tecla">Enter</span> para salir de MAS.</li>
</ol>

{fig('figura-mas1.png', 'El menú de MAS', 18,
     'El menú de MAS. Está en inglés, pero solo hacen falta tres números: el <b>2</b> '
     '(Ohook — Office) para activar, el <b>5</b> para comprobar el estado y el <b>0</b> '
     'para salir. El <b>1</b> es para Windows y aquí no corresponde.')}

{fig('figura-mas2.png', 'La señal de éxito de MAS', 19,
     'La señal de que salió bien: la frase en verde <i>«Office is permanently activated»</i>. '
     'Debajo, en gris, avisa de que Word y Excel ya están activados y de que puede ignorarse '
     'el botón «Buy» de Office.')}

<h4 class="paso">Paso I. Comprobar que quedó activado</h4>
<ol class="pasos">
  <li>En el menú del instalador escriba <span class="num">6</span> → <span class="tecla">Enter</span>.</li>
  <li>Busque la línea <code>LICENSE STATUS</code>. Si dice <code>---LICENSED---</code>,
      está activado.</li>
</ol>

{fig('figura-14.png', 'Comprobar la licencia', 20,
     'El recuadro muestra qué versión está instalada. La flecha de abajo señala la línea '
     'que confirma la activación.')}

<p class="chico">También puede comprobarse desde el propio Word: se abre → <b>Archivo</b> →
<b>Cuenta</b>. Debe indicar que el producto está activado.</p>

<h4 class="paso">Paso J. Cerrar todo con calma</h4>
<ol class="pasos">
  <li>En el menú escriba <span class="num">9</span> → <span class="tecla">Enter</span>.</li>
  <li>Presione cualquier tecla cuando aparezca el mensaje verde de despedida.</li>
  <li>Cierre la ventana de PowerShell con la <b>X</b> de la esquina superior derecha.</li>
  <li>Si se trabajó en el laboratorio, restaure el snapshot al terminar.</li>
</ol>

<h3 class="salto">5. Errores frecuentes y cómo resolverlos</h3>
<p class="chico">Estos son los mensajes que aparecen con más frecuencia. En cada caso se
indica el texto exacto del error, por qué ocurre y qué hay que hacer.</p>

<h4>5.1 · El error más común: la ejecución de scripts está deshabilitada</h4>
<div class="errbox">No se puede cargar el archivo office-isupol.ps1 porque la ejecución de
scripts está deshabilitada en este sistema. Para obtener más información, consulte
about_Execution_Policies en https:/go.microsoft.com/fwlink/?LinkID=135170.<br>
+ CategoryInfo : SecurityError: (:) [], PSSecurityException<br>
+ FullyQualifiedErrorId : UnauthorizedAccess</div>
<p class="chico"><b>Por qué ocurre:</b> Windows trae bloqueada por seguridad la ejecución
de scripts. Es una configuración del sistema, no un problema del instalador.<br>
<b>Cómo se soluciona:</b> escriba este comando en la misma ventana y pulse
<span class="tecla">Enter</span>. Solo afecta a esa ventana y todo vuelve a la normalidad
al cerrarla:</p>
<div class="comando">Set-ExecutionPolicy Bypass -Scope Process -Force</div>
<p class="chico">Después vuelva a pegar el comando del <b>Paso C</b> y pulse
<span class="tecla">Enter</span>.</p>

<h4>5.2 · El término «irm» no se reconoce</h4>
<div class="errbox">'irm' no se reconoce como un comando interno o externo,<br>
programa o archivo por lotes ejecutable.</div>
<p class="chico"><b>Por qué ocurre:</b> el comando se pegó en el <i>Símbolo del sistema</i>
(CMD), que es una ventana negra parecida pero distinta.<br>
<b>Cómo se soluciona:</b> cierre esa ventana y abra <b>PowerShell</b> siguiendo el
<b>Paso B</b>. PowerShell tiene el fondo azul oscuro y su título empieza por
<code>{PROMPT2}</code>.</p>

<h4>5.3 · No se puede establecer la conexión</h4>
<div class="errbox">Invoke-RestMethod : No se puede establecer un canal seguro para SSL/TLS
con la autoridad 'raw.githubusercontent.com'.</div>
<p class="chico"><b>Por qué ocurre:</b> un Windows 10 sin actualizar intenta conectarse con
un protocolo de seguridad antiguo que los servidores ya no aceptan.<br>
<b>Cómo se soluciona:</b> escriba primero esta línea y pulse
<span class="tecla">Enter</span>; después vuelva a pegar el comando del Paso C:</p>
<div class="comando">[Net.ServicePointManager]::SecurityProtocol = 'Tls12'</div>

<h4>5.4 · Faltan permisos de administrador</h4>
<p class="chico">El propio instalador lo detecta y se detiene con este aviso:</p>

{fig('figura-16.png', 'Error de permisos', 21,
     'Así se ve el aviso cuando faltan permisos de administrador. El programa indica '
     'exactamente qué hacer; la flecha señala la instrucción.')}

<p class="chico"><b>Por qué ocurre:</b> PowerShell se abrió con la opción «Abrir» en lugar
de «Ejecutar como administrador».<br>
<b>Cómo se soluciona:</b> cierre la ventana y repita el <b>Paso B</b>.</p>

<h4>5.5 · Otros avisos</h4>
<table class="tab">
  <tr><th style="width:36%">Lo que aparece</th><th>Qué hacer</th></tr>
  <tr><td>«SIN CONEXIÓN A INTERNET»</td>
      <td>Revise el cable o el WiFi. Hace falta conexión para descargar Office de Microsoft.</td></tr>
  <tr><td>«ESPACIO INSUFICIENTE EN EL DISCO»</td>
      <td>Libere al menos 5 GB (vacíe la papelera o borre archivos grandes) y ejecute de nuevo el comando.</td></tr>
  <tr><td>«ESTE EQUIPO NO ES COMPATIBLE»</td>
      <td>El equipo tiene un Windows anterior al 10. Office 2019, 2021 y 2024 no se pueden instalar ahí.</td></tr>
  <tr><td>«ESA OPCIÓN NO EXISTE»</td>
      <td>Se escribió una letra o un número fuera del 1 al 9. Vuelva a intentarlo.</td></tr>
  <tr><td>Los bordes salen como símbolos raros</td>
      <td>La ventana no está mostrando los caracteres correctamente. Cierre y vuelva a abrir
          PowerShell; si persiste, escriba <code>chcp 65001</code> y ejecute otra vez el comando.</td></tr>
  <tr><td>Parece congelado durante la instalación</td>
      <td>Observe el reloj que va contando (Figura 14). Si avanza, el programa está trabajando.</td></tr>
  <tr><td>El antivirus bloquea MAS</td>
      <td>Es lo más frecuente al activar y está explicado en el <b>Paso H</b>.</td></tr>
  <tr><td>La ventana se cerró sola a mitad de la instalación</td>
      <td>Office quedó a medias. Abra de nuevo PowerShell como administrador, ejecute el
          comando y elija la misma versión: el instalador retoma el trabajo.</td></tr>
</table>

<h3>6. Cuidado con la opción 7</h3>
<p class="chico">La opción <span class="num">7</span> borra Office del equipo. Para que
nadie la ejecute sin querer, aquí los números están <b>al revés</b> que en el resto del
programa: el <b>1 cancela</b> y solo el <b>2</b> borra.</p>

{fig('figura-15.png', 'Desinstalar Office', 22,
     'El recuadro avisa del cambio de orden. Las flechas señalan cada opción: conviene '
     'fijarse bien antes de escribir. Los documentos no se borran, solo los programas.')}

<div class="resumen"><b>Resumen en una frase:</b> se enciende el equipo → se abre
PowerShell <b>como administrador</b> → se copia el comando de este manual → clic derecho
para pegarlo → <span class="tecla">Enter</span> → se escribe el número de la versión (por
ejemplo <b>3</b>) → se escribe <b>1</b> para confirmar → se espera el cartel verde → se
escribe <b>5</b> para activar → <b>1</b> para abrir MAS → dentro de MAS <b>2</b> → se
espera la línea verde → <b>0</b> para salir de MAS → <b>6</b> para comprobar → <b>9</b>
para salir. ¡Listo!</div>

<div class="peligro"><b>Recordatorio importante:</b> este manual sirve para aprender y
practicar en un entorno de laboratorio. Activar productos para no pagar la licencia va
contra los términos de Microsoft. La idea es entender cómo funciona, con responsabilidad.</div>

<h3>Bibliografía</h3>
<p style="font-size:8.5pt; line-height:1.45">
Microsoft. (2024). <i>Configuration options for the Office Deployment Tool</i>. Microsoft Learn.
https://learn.microsoft.com/microsoft-365-apps/deploy/office-deployment-tool-configuration-options<br>
Microsoft. (2025). <i>Product IDs supported by the Office Deployment Tool for Click-to-Run</i>. Microsoft Learn.
https://learn.microsoft.com/previous-versions/troubleshoot/microsoft-365/microsoft-365-apps/office-suite-problems/product-ids-supported-office-deployment-click-to-run<br>
Microsoft. (2024). <i>about_Execution_Policies</i>. Microsoft Learn.
https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_execution_policies<br>
Microsoft. (2024). <i>Update channel for Office LTSC 2021</i>. Microsoft Learn.
https://learn.microsoft.com/office/ltsc/2021/update<br>
Massgrave. (2026). <i>Microsoft Activation Scripts (MAS)</i>. https://massgrave.dev
</p>

<div class="pie"><b>Sobre las imágenes.</b> Las pantallas del instalador, de PowerShell y
de MAS reproducen el texto literal de cada programa. Las figuras 1 y 2 (menú Inicio y aviso
de permisos) son recreaciones de las pantallas de Windows: pueden variar ligeramente según
la versión instalada.<br><br>
Manual de usuario paso a paso desde cero · Instalador de Office ISUPOL ·
Material educativo para practicar en un entorno de laboratorio.<br>
El instalador descarga Office únicamente de los servidores oficiales de Microsoft
(officecdn.microsoft.com y c2rsetup.officeapps.live.com).</div>

</body>
</html>
"""

# estilos nuevos: bloque de comando y caja de error
css = css.replace('</style>', """
  .comando { background: #0d1117; color: #e6edf3; font-family: "DejaVu Sans Mono", monospace;
             font-size: 8.5pt; padding: 11px 13px; border-radius: 6px; margin: 10px 0;
             word-break: break-all; line-height: 1.6; border: 1px solid #30363d; }
  .errbox { background: #1a1a1a; color: #ff6b6b; font-family: "DejaVu Sans Mono", monospace;
            font-size: 7.8pt; padding: 10px 12px; border-radius: 5px; margin: 9px 0;
            line-height: 1.5; border-left: 4px solid #c0392b; }
  h4 { font-family: "DejaVu Sans", sans-serif; font-size: 10.5pt; margin: 16px 0 6px;
       color: #0d3b66; page-break-after: avoid; }
</style>""")

P.write_text(css + cuerpo, encoding='utf-8')
print('manual generado | figuras:', cuerpo.count('<img src='), '| iconos:', cuerpo.count('<svg'))
