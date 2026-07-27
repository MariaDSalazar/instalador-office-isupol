#!/usr/bin/env python3
"""Replica las funciones de dibujo de office-isupol.ps1 y las renderiza a PNG.
Genera dos juegos:
  pantalla-pN.png  limpias
  figura-NN.png    con recuadros rojos y numeros, para el manual
Check: si una caja se desalinea o falta un texto anclado, el assert falla."""
import math
from PIL import Image, ImageDraw, ImageFont

ANCHO, W = 66, 75
FUENTE = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
FUENTE_B = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
ROJO = '#E01B24'

C = {'Black': '#0C0C0C', 'DarkCyan': '#3A96DD', 'DarkGray': '#767676',
     'Gray': '#CCCCCC', 'Green': '#16C60C', 'Cyan': '#61D6D6', 'Red': '#E74856',
     'Magenta': '#B4009E', 'Yellow': '#F9F1A5', 'White': '#F2F2F2',
     'DarkYellow': '#C19C00'}

# ------------------------------------------------------------ primitivas
def lin(car, izq, der, color='DarkCyan'):
    return [('  ' + izq + car * (ANCHO + 2) + der, color)]

def fila(texto, color='White', borde='DarkCyan', v='│'):
    return [('  ' + v + ' ', borde), (texto.ljust(ANCHO), color), (' ' + v, borde)]

def centro(texto, color='White', borde='DarkCyan', v='│'):
    return fila(' ' * max(0, (ANCHO - len(texto)) // 2) + texto, color, borde, v)

def dato(et, val, color='White', v='│'):
    return [('  ' + v + ' ', 'DarkCyan'), (et.ljust(16), 'Gray'),
            (val.ljust(ANCHO - 16), color), (' ' + v, 'DarkCyan')]

def titulo(t):
    return [[], [('   ' + t, 'White')], [('   ' + '─' * len(t), 'DarkCyan')]]

def barra(frac, texto):
    n, lleno = 38, int(frac * 38)
    return [('   ', 'White'), ('[', 'DarkGray'), ('█' * lleno, 'Green'),
            ('░' * (n - lleno), 'DarkGray'), (']', 'DarkGray'),
            (' %3d%%  ' % (frac * 100), 'Cyan'), (texto.ljust(24), 'Gray')]

def v(): return []

def preguntar(pregunta, t1, t2, c1='Green', c2='Red', elegido='1'):
    return [v(), [('   ' + pregunta, 'White')],
            [('      1  ', c1), (t1, 'White')],
            [('      2  ', c2), (t2, 'White')], v(),
            [('   Escribe 1 o 2 y pulsa Enter: ', 'White'),
             (elegido, 'Yellow'), ('▌', 'Gray')]]

def portada():
    return [v(), lin('═', '╔', '╗'),
        centro('INSTITUTO SUPERIOR TECNOLÓGICO', 'Cyan', 'DarkCyan', '║'),
        centro('POLICÍA NACIONAL', 'Cyan', 'DarkCyan', '║'),
        centro('Prevención del Delito y Seguridad Ciudadana', 'DarkGray', 'DarkCyan', '║'),
        lin('─', '╟', '╢'),
        dato('  Asignatura', 'Competencias Digitales          Unidad 1 de 3', 'White', '║'),
        dato('  Docente', 'Mgtr. María del Carmen Salazar Torres', 'White', '║'),
        dato('  Sección', 'C', 'White', '║'),
        lin('─', '╟', '╢'),
        centro('INSTALADOR DE OFFICE', 'Yellow', 'DarkCyan', '║'),
        centro('Descarga directa desde los servidores de Microsoft', 'DarkGray', 'DarkCyan', '║'),
        lin('═', '╚', '╝')]

def aviso(t, ls, color='Yellow'):
    out = [v(), lin('═', '╔', '╗', color), fila('  (!)  ' + t, color, color, '║'),
           lin('─', '╟', '╢', color)]
    out += [fila('       ' + l, 'White', color, '║') for l in ls]
    return out + [lin('═', '╚', '╝', color), v()]

def exito(t, ls):
    out = [v(), lin('═', '╔', '╗', 'Green'), centro(t, 'Green', 'Green', '║'),
           lin('─', '╟', '╢', 'Green')]
    out += [fila('       ' + l, 'White', 'Green', '║') for l in ls]
    return out + [lin('═', '╚', '╝', 'Green'), v()]

CAT = [('1', 'Office 2016 Professional Plus', '2.5 GB', 'Suite completa'),
       ('2', 'Office 2019 Professional Plus', '1.8 GB', 'Word Excel PPT'),
       ('3', 'Office LTSC 2021 Professional Plus', '1.9 GB', 'Word Excel PPT'),
       ('4', 'Office LTSC 2024 Professional Plus', '2.1 GB', 'Word Excel PPT')]

OTRAS = [('5', 'Activar Office con MAS  (massgrave.dev)', 'Cyan'),
         ('6', 'Ver qué Office tengo y si está activado', 'Cyan'),
         ('7', 'Desinstalar Office de este equipo', 'DarkYellow'),
         ('8', 'Ayuda: qué hace cada opción', 'Gray'),
         ('9', 'Salir del programa', 'Red')]

def menu(elegido='3'):
    out = [v(), [('   INSTALAR OFFICE', 'White')],
        [('  ┌─────┬─────────────────────────────────────┬──────────┬────────────────┐', 'DarkCyan')],
        [('  │  #  │ Versión                             │  Descarga│ Aplicaciones   │', 'Gray')],
        [('  ├─────┼─────────────────────────────────────┼──────────┼────────────────┤', 'DarkCyan')]]
    for k, nom, peso, apps in CAT:
        out.append([('  │  ', 'DarkCyan'), (k, 'Green'), ('  │ ', 'DarkCyan'),
                    (nom.ljust(36), 'White'), ('│ ', 'DarkCyan'),
                    (('≈ ' + peso).ljust(9), 'Yellow'), ('│ ', 'DarkCyan'),
                    (apps.ljust(15), 'Gray'), ('│', 'DarkCyan')])
    out += [[('  └─────┴─────────────────────────────────────┴──────────┴────────────────┘', 'DarkCyan')],
        v(), [('   OTRAS OPCIONES', 'White')],
        [('  ┌─────┬─────────────────────────────────────────────────────────────────┐', 'DarkCyan')]]
    for k, txt, col in OTRAS:
        out.append([('  │  ', 'DarkCyan'), (k, col), ('  │ ', 'DarkCyan'),
                    (txt.ljust(64), 'White'), ('│', 'DarkCyan')])
    out += [[('  └─────┴─────────────────────────────────────────────────────────────────┘', 'DarkCyan')],
        v(), [('   Escribe el número de la opción y pulsa Enter: ', 'White'),
              (elegido, 'Yellow'), ('▌', 'Gray')]]
    return out

def revision(office='no instalado'):
    return titulo('Revisión del equipo') + [lin('─', '┌', '┐'),
        dato('  Sistema', 'Windows 11  (build 26100)', 'Green'),
        dato('  Arquitectura', '64 bits'),
        dato('  Permisos', 'Administrador', 'Green'),
        dato('  Espacio en C:', '184.2 GB libres', 'Green'),
        dato('  Defender', 'Protección en tiempo real activa', 'Gray'),
        dato('  Office', office, 'Gray'),
        lin('─', '└', '┘')]

# -------------------------------------------------------------- pantallas
P1 = portada() + revision() + menu()

P2 = (titulo('Resumen de lo que se va a instalar') + [lin('─', '┌', '┐'),
    dato('  Versión', 'Office LTSC 2021 Professional Plus', 'Cyan'),
    dato('  Aplicaciones', 'Word Excel PPT'),
    dato('  Idioma', 'Español (es-es)'),
    dato('  Arquitectura', '64 bits'),
    dato('  Descarga', 'aproximadamente 1.9 GB'),
    lin('─', '└', '┘')]
    + aviso('NO CIERRES ESTA VENTANA', [
        'La descarga y la instalación tardan entre 10 y 30',
        'minutos según tu internet.', '',
        'Cierra Word, Excel y PowerPoint antes de continuar.',
        'El script te avisará en verde cuando puedas cerrar.'])
    + preguntar('¿Quieres instalarlo ahora?',
                'Sí, empezar la instalación', 'No, volver al menú'))

P3 = ([v(), [('   [1/3] ', 'Yellow'), ('Descargando el instalador oficial de Microsoft', 'White')],
    barra(0.47, '3.4 / 7.3 MB'), v(),
    [('   [2/3] ', 'Yellow'), ('Preparando la configuración de la instalación', 'White')],
    [('   ✓  configuration.xml listo', 'Green')], v(),
    [('   [3/3] ', 'Yellow'), ('Instalando Office (se abrirá la ventana azul de Microsoft)', 'White')],
    v(), [('   ⠹  Descargando e instalando Office  ·  transcurrido 07:41', 'Cyan')]]
    + exito('OFFICE INSTALADO CORRECTAMENTE', [
        'Office LTSC 2021 Professional Plus', '',
        'Ahora elige la opción 5 del menú para activarlo.'])
    + [[('   Presiona cualquier tecla para volver al menú...', 'Green')]])

P4 = (titulo('Activar Office con MAS')
    + aviso('ANTES DE ACTIVAR', [
        'Windows Defender detecta a MAS como herramienta de',
        'activación y puede bloquearlo. Es un falso positivo',
        'conocido, avisado en la propia web massgrave.dev.', '',
        'Si te lo bloquea: Seguridad de Windows → Protección',
        'antivirus → Administrar la configuración → apaga la',
        'Protección en tiempo real, activa Office, y vuelve',
        'a encenderla al terminar.'], 'DarkYellow')
    + [[('   Se abrirá el menú de MAS. Dentro de él:', 'White')],
       [('      2 = activar Office      5 = ver estado      0 = salir de MAS', 'Gray')]]
    + preguntar('¿Abrir MAS ahora?', 'Sí, abrir MAS', 'No, volver al menú'))

P5 = (titulo('Office instalado en este equipo') + [lin('─', '┌', '┐'),
    dato('  Producto', 'ProPlus2021Volume', 'Cyan'),
    dato('  Versión', '16.0.14332.20721'),
    dato('  Idioma', 'es-es'),
    dato('  Arquitectura', 'x64'),
    lin('─', '└', '┘'), v(),
    [('   Estado de la licencia:', 'White')],
    [('     LICENSE NAME: Office 21, Office21ProPlus2021VL_KMS_Client edition', 'Gray')],
    [('     LICENSE STATUS:  ---LICENSED---', 'Gray')],
    [('     Remaining Windows rearm count: 1', 'Gray')], v(),
    [('   Presiona cualquier tecla para volver al menú...', 'Green')]])

P6 = (titulo('Qué hace este programa') + [lin('─', '┌', '┐'),
    fila('  Este instalador descarga Office directamente de los'),
    fila('  servidores de Microsoft. No usa páginas de terceros'),
    fila('  ni archivos de dudosa procedencia.'),
    fila(''),
    fila('  Opciones 1 a 4   Instalan la versión que elijas. Solo'),
    fila('                   Word, Excel y PowerPoint (menos la'),
    fila('                   2016, que instala la suite completa'),
    fila('                   porque Microsoft no deja elegir).'),
    fila(''),
    fila('  Opción 5         Abre MAS (massgrave.dev) para activar.'),
    fila('  Opción 6         Muestra qué Office tienes y su licencia.'),
    fila('  Opción 7         Borra Office del equipo.'),
    fila(''),
    fila('  Es material de laboratorio para la asignatura.', 'DarkGray'),
    fila('  Al terminar la práctica, restaura el snapshot.', 'DarkGray'),
    lin('─', '└', '┘'), v(),
    [('   Presiona cualquier tecla para volver al menú...', 'Green')]])

P7 = (titulo('Desinstalar Office de este equipo')
    + aviso('ESTO BORRA OFFICE DEL EQUIPO', [
        'Se quitarán Word, Excel, PowerPoint y lo demás.',
        'Tus documentos NO se borran, solo los programas.', '',
        'Fíjate bien: aquí el 1 es CANCELAR.'], 'Red')
    + preguntar('¿Seguro que quieres borrar Office?',
                'No, cancelar y volver al menú',
                'Sí, borrar Office de este equipo', 'Green', 'Red', '1'))

P8 = ([v()] + aviso('FALTAN PERMISOS DE ADMINISTRADOR', [
        'Cierra esta ventana.',
        'Pulsa la tecla Windows, escribe  PowerShell,',
        'y elige  "Ejecutar como administrador".',
        'Después vuelve a abrir este instalador.'], 'Red')
    + [[('   Presiona cualquier tecla para cerrar...', 'Green')]])

# --- PowerShell recien abierta y con el comando pegado -------------------
AZUL_PS = '#012456'
CMD = 'irm https://raw.githubusercontent.com/MariaDSalazar/instalador-office-isupol/main/office-isupol.ps1 | iex'

PS0 = [v(),
    [('Windows PowerShell', 'White')],
    [('Copyright (C) Microsoft Corporation. Todos los derechos reservados.', 'White')],
    v(),
    [('Instale la nueva PowerShell para mejorar la compatibilidad multiplataforma', 'White')],
    [('https://aka.ms/PSWindows', 'White')],
    v(),
    [('PS C:\\Windows\\system32> ', 'White'), ('▌', 'Gray')]]

# el comando es largo: se parte en dos lineas como hace la consola real
PS1 = PS0[:-1] + [
    [('PS C:\\Windows\\system32> ', 'White'), (CMD[:52], 'Yellow')],
    [(CMD[52:], 'Yellow'), ('▌', 'Gray')]]


# --- menu de MAS 3.12, copiado literal de MAS_AIO.cmd --------------------
def _mas_op(num, nombre, resto, verde=True):
    return [('             [' + num + '] ', 'White'),
            (nombre.ljust(20), 'Green' if verde else 'White'), (resto, 'White')]

MAS = [v(),
    [('       ' + '_' * 62, 'White')], v(),
    [('                 Activation Methods:', 'White')], v(),
    _mas_op('1', 'HWID', '- Windows'),
    _mas_op('2', 'Ohook', '- Office'),
    _mas_op('3', 'TSforge', '- Windows / Office / ESU'),
    _mas_op('4', 'Online KMS', '- Windows / Office', False),
    [('             ' + '_' * 50, 'White')], v(),
    [('             [5] Check Activation Status', 'White')],
    [('             [6] Change Windows Edition', 'White')],
    [('             [7] Change Office Edition', 'White')],
    [('             ' + '_' * 50, 'White')], v(),
    [('             [8] Troubleshoot', 'White')],
    [('             [E] Extras', 'White')],
    [('             [H] Help', 'White')],
    [('             [0] Exit', 'White')],
    [('       ' + '_' * 62, 'White')], v(),
    [('         ', 'White'),
     ('Choose a menu option using your keyboard [1,2,3...E,H,0] :', 'Green')]]

# --- pantalla de exito de Ohook (texto literal de MAS) -------------------
MASOK = [v(), v(),
    [('Office is permanently activated.', 'Green')],
    [("Office apps such as Word, Excel are activated, use them directly.", 'Gray')],
    [("Ignore 'Buy' button in Office dashboard app.", 'Gray')],
    [('Help: https://massgrave.dev/troubleshoot', 'White')], v(),
    [('Press any key to go back to main menu...', 'White')]]

PANTALLAS = [('P1', P1), ('P2', P2), ('P3', P3), ('P4', P4),
             ('P5', P5), ('P6', P6), ('P7', P7), ('P8', P8),
             ('PS0', PS0), ('PS1', PS1), ('MAS', MAS), ('MASOK', MASOK)]

# ------------------------------------------------------------------ util
def idx(pantalla, sub):
    """Indice de la primera linea que contiene sub. Falla si no existe:
    asi una figura no puede quedar apuntando a algo que ya no esta."""
    for i, l in enumerate(pantalla):
        if sub in ''.join(s for s, _ in l):
            return i
    raise ValueError('no encontrado en la pantalla: ' + sub)

def recortar(pantalla, marcas, flechas, desde, hasta):
    """Deja solo las filas [desde, hasta) y reajusta marcas y flechas.
    Evita que una figura arrastre media pantalla que no viene al caso."""
    m = [(n, f1 - desde, f2 - desde, c1, c2) for n, f1, f2, c1, c2 in marcas]
    f = [(t, fi - desde, c) for t, fi, c in flechas]
    assert all(0 <= f1 and f2 < hasta - desde for _, f1, f2, _, _ in m), 'marca fuera del recorte'
    assert all(0 <= fi < hasta - desde for _, fi, _ in f), 'flecha fuera del recorte'
    return pantalla[desde:hasta], m, f


def check():
    for nombre, p in PANTALLAS:
        anchos = set()
        for linea in p:
            txt = ''.join(s for s, _ in linea)
            if txt.strip() and any(c in txt for c in '│║┌└╔╚├┬'):
                anchos.add(len(txt))
        assert anchos <= {72, 75}, f'{nombre}: cajas desalineadas -> {sorted(anchos)}'
    print('CHECK cajas: OK')

# --------------------------------------------------------------- render
def punta(d, x1, y1, x2, y2, color=ROJO, w=5):
    """Linea de (x1,y1) a (x2,y2) con punta de flecha en el extremo."""
    d.line([x1, y1, x2, y2], fill=color, width=w)
    ang = math.atan2(y2 - y1, x2 - x1)
    for lado in (1, -1):
        a = ang + lado * math.radians(155)
        d.line([x2, y2, x2 + 20 * math.cos(a), y2 + 20 * math.sin(a)], fill=color, width=w)


def render(pantalla, salida, marcas=(), flechas=(),
           titulo_ventana='Administrador: ISUPOL  ·  Instalador de Office',
           fondo=None):
    fs = 26
    font = ImageFont.truetype(FUENTE, fs)
    fnum = ImageFont.truetype(FUENTE_B, 30)
    cw, lh, pad, bh = font.getlength('M'), int(fs * 1.32), 26, 40
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    margen = 64 if (marcas or flechas) else 0   # sitio para los circulos numerados
    fetq = ImageFont.truetype(FUENTE_B, 21)
    # Una flecha que apunta a la mitad izquierda sale por la izquierda: si no,
    # cruzaria toda la pantalla tachando el texto.
    izqs = [f for f in flechas if f[2] < 35]
    ders = [f for f in flechas if f[2] >= 35]
    anchura = lambda fs: int(max(max(d0.textlength(l, font=fetq)
                                     for l in t.split('\n')) for t, _, _ in fs)) + 150
    extra_izq = anchura(izqs) if izqs else 0
    dcha = anchura(ders) if ders else 0
    iw = int(cw * W) + pad * 2 + margen + extra_izq + dcha
    ih = lh * len(pantalla) + pad * 2 + bh + (60 if flechas else 0)
    im = Image.new('RGB', (iw, ih), fondo or C['Black'])
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, iw, bh], fill='#2B2B2B')
    d.text((pad, 10), titulo_ventana, font=ImageFont.truetype(FUENTE, 18), fill='#DDDDDD')
    for i, col in enumerate(('#5A5A5A', '#5A5A5A', '#C05050')):
        d.rectangle([iw - 34 * (3 - i) - 8, 14, iw - 34 * (3 - i) + 6, 28], fill=col)

    x0 = pad + margen + extra_izq
    y = pad + bh
    for linea in pantalla:
        x = x0
        for txt, col in linea:
            d.text((x, y), txt, font=font, fill=C[col])
            x += cw * len(txt)
        y += lh

    # marcas: (num, fila_ini, fila_fin, col_ini, col_fin)
    for num, f1, f2, c1, c2 in marcas:
        rx1 = x0 + cw * c1 - 6
        ry1 = pad + bh + lh * f1 - 4
        rx2 = x0 + cw * c2 + 6
        ry2 = pad + bh + lh * (f2 + 1) + 2
        d.rounded_rectangle([rx1, ry1, rx2, ry2], radius=8, outline=ROJO, width=4)
        cx, cy, r = rx1 - 28, (ry1 + ry2) / 2, 24
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ROJO)
        tw = d.textlength(str(num), font=fnum)
        d.text((cx - tw / 2, cy - 20), str(num), font=fnum, fill='white')

    # flechas: (texto, fila, columna a la que apunta)
    # Las etiquetas se apilan sin pisarse: si la siguiente cae encima de la
    # anterior se empuja hacia abajo y la flecha sale en diagonal.
    ALTO_L = 26
    for lado, grupo in (('der', ders), ('izq', izqs)):
        fondo = pad + bh - 10               # y ocupada hasta ahora en esta columna
        for texto, fila, col in sorted(grupo, key=lambda f: f[1]):
            lineas = texto.split('\n')
            alto = len(lineas) * ALTO_L
            ty = pad + bh + lh * fila + lh / 2      # punto al que apunta
            y_t = max(ty - alto / 2, fondo + 14)
            fondo = y_t + alto
            if lado == 'der':
                ex = x0 + cw * W + 34
                punta(d, ex, y_t + alto / 2, x0 + cw * col + 10, ty)
                tx_txt = ex + 14
            else:
                ancho_t = max(d0.textlength(l, font=fetq) for l in lineas)
                ex = pad + ancho_t + 20
                punta(d, ex, y_t + alto / 2, x0 + cw * col - 6, ty)
                tx_txt = pad
            for l in lineas:
                d.text((tx_txt, y_t), l, font=fetq, fill=ROJO)
                y_t += ALTO_L

    im.save(salida)
    return salida.rsplit('/', 1)[-1]

# --------------------------------------------------------------- figuras
# Cada figura: (archivo, pantalla, marcas, flechas)
#   marca  = (numero, fila_ini, fila_fin, col_ini, col_fin)
#   flecha = (texto, fila, columna a la que apunta)
# Todo se ancla por texto con idx(): si una frase del script cambia, esto revienta
# en vez de dejar una flecha apuntando al sitio equivocado.

def figuras():
    F = []

    # --- el menu de MAS ya abierto
    F.append(('figura-mas1.png', MAS, [], [
        ('ESCRIBE EL 2\npara activar Office',
         idx(MAS, '[2] Ohook'), 13),
        ('El 5 sirve para comprobar\nsi quedo activado',
         idx(MAS, '[5] Check Activation'), 13),
        ('El 0 para salir de MAS',
         idx(MAS, '[0] Exit'), 13)]))

    # --- la senal de exito de MAS
    F.append(('figura-mas2.png', MASOK, [], [
        ('ESTA LINEA VERDE\nes la senal de que\nOffice quedo activado',
         idx(MASOK, 'permanently activated'), 33)]))

    # --- PowerShell recien abierta como administrador
    F.append(('figura-ps1.png', PS0, [], [
        ('Aqui escribe el sistema.\nAqui vas a pegar el comando',
         idx(PS0, 'PS C:'), 26)]))

    # --- el comando ya pegado, listo para pulsar Enter
    F.append(('figura-ps2.png', PS1, [], [
        ('El comando pegado.\nSolo falta pulsar Enter',
         idx(PS1, 'main/office-isupol.ps1'), 45)]))

    # --- 1. la portada, para reconocer que abrio el programa correcto
    F.append(('figura-01.png', P1, [], [
        ('El nombre del Instituto:\nsi lo ves, abriste\nel programa correcto',
         idx(P1, 'INSTITUTO SUPERIOR'), 60),
        ('Aqui dice que Office se\nbaja de Microsoft',
         idx(P1, 'Descarga directa desde'), 68)]))

    # --- 2. revision del equipo, dato por dato
    F.append(('figura-02.png', P1, [
        (1, idx(P1, 'Revisión del equipo'), idx(P1, '  Office'), 2, 71)], [
        ('Tu version de Windows.\nDebe ser 10 u 11',
         idx(P1, '  Sistema'), 50),
        ('ESTO ES LO IMPORTANTE:\ndebe decir Administrador\ny estar en VERDE',
         idx(P1, '  Permisos'), 50),
        ('Espacio libre.\nHacen falta 5 GB',
         idx(P1, '  Espacio en C:'), 50),
        ('Te dice si ya tienes\nOffice instalado',
         idx(P1, '  Office'), 50)]))

    # --- 3. la tabla de versiones
    F.append(('figura-03.png', P1, [
        (1, idx(P1, '   INSTALAR OFFICE'),
            idx(P1, '└─────┴─────────────────────────────────────┴'), 2, 74)], [
        ('Este numero es el\nque vas a escribir',
         idx(P1, 'Office 2016 Professional'), 5),
        ('SI NO SABES CUAL:\nelige la 3',
         idx(P1, 'Office LTSC 2021 Professional'), 5),
        ('Aqui ves cuanto pesa\ncada version y que\nprogramas trae',
         idx(P1, '│  #  │ Versión'), 76)]))

    # --- 4. las otras opciones del menu
    F.append(('figura-04.png', P1, [
        (1, idx(P1, '   OTRAS OPCIONES'),
            idx(P1, '└─────┴──────────────────────────────────────────────'), 2, 74)], [
        ('Para ACTIVAR Office\ndespues de instalarlo',
         idx(P1, 'Activar Office con MAS'), 72),
        ('Para comprobar que\nquedo activado',
         idx(P1, 'Ver qué Office tengo'), 72),
        ('CUIDADO: esta borra Office',
         idx(P1, 'Desinstalar Office de este'), 72),
        ('Para cerrar el programa',
         idx(P1, 'Salir del programa'), 72)]))

    # --- 5. donde se escribe el numero
    F.append(('figura-05.png', P1, [], [
        ('AQUI escribes el numero\ncon el teclado y pulsas\nla tecla Enter',
         idx(P1, 'Escribe el número de la opción'), 50)]))

    # --- 6. resumen antes de instalar
    F.append(('figura-06.png', P2, [
        (1, idx(P2, '  Versión'), idx(P2, '  Descarga'), 2, 71)], [
        ('Comprueba que sea la\nversion que elegiste',
         idx(P2, '  Versión'), 55),
        ('Los programas que\nse van a instalar',
         idx(P2, '  Aplicaciones'), 55),
        ('Cuanto se va a descargar',
         idx(P2, '  Descarga'), 55)]))

    # --- 7. el aviso de no cerrar
    F.append(('figura-07.png', P2, [
        (1, idx(P2, 'NO CIERRES ESTA VENTANA'),
            idx(P2, 'El script te avisará en verde'), 2, 71)], [
        ('LEE ESTO ANTES\nDE CONTINUAR',
         idx(P2, 'NO CIERRES ESTA VENTANA'), 45),
        ('Cierra Word y Excel\nsi los tienes abiertos',
         idx(P2, 'Cierra Word, Excel y PowerPoint'), 68)]))

    # --- 8. la confirmacion 1 / 2
    F.append(('figura-08.png', P2, [
        (1, idx(P2, '¿Quieres instalarlo ahora?'), idx(P2, 'Escribe 1 o 2'), 3, 52)], [
        ('Escribe 1 para\nempezar a instalar',
         idx(P2, 'Sí, empezar la instalación'), 40),
        ('Escribe 2 si te\narrepentiste',
         idx(P2, 'No, volver al menú'), 40),
        ('Aqui aparece lo que\nescribes. Luego Enter',
         idx(P2, 'Escribe 1 o 2'), 40)]))

    # --- 9. la barra de descarga
    F.append(('figura-09.png', P3, [], [
        ('La barra verde se va\nllenando sola',
         idx(P3, '3.4 / 7.3 MB'), 20),
        ('El porcentaje: va de 0 a 100',
         idx(P3, '3.4 / 7.3 MB'), 47),
        ('Cuantos MB lleva\ndescargados',
         idx(P3, '3.4 / 7.3 MB'), 60)]))

    # --- 10. la espera de la instalacion
    F.append(('figura-10.png', P3, [], [
        ('Paso 1: baja el instalador',
         idx(P3, 'Descargando el instalador oficial'), 60),
        ('Paso 2: prepara la\nconfiguracion',
         idx(P3, 'configuration.xml listo'), 40),
        ('Paso 3: instala Office.\nMientras este reloj avance,\nTODO VA BIEN. Ten paciencia',
         idx(P3, 'transcurrido'), 58)]))

    # --- 11. la senal de exito
    F.append(('figura-11.png', P3, [
        (1, idx(P3, 'OFFICE INSTALADO CORRECTAMENTE'),
            idx(P3, 'Ahora elige la opción 5'), 2, 71)], [
        ('ESTA ES LA SENAL\nDE QUE SALIO BIEN',
         idx(P3, 'OFFICE INSTALADO CORRECTAMENTE'), 50),
        ('Te dice cual es el\nsiguiente paso',
         idx(P3, 'Ahora elige la opción 5'), 60)]))

    # --- 12. aviso del antivirus antes de MAS
    F.append(('figura-12.png', P4, [
        (1, idx(P4, 'ANTES DE ACTIVAR'), idx(P4, 'a encenderla al terminar'), 2, 71)], [
        ('Si el antivirus lo bloquea,\nno es un virus de verdad',
         idx(P4, 'activación y puede bloquearlo'), 60),
        ('Estos son los pasos\npara apagarlo un rato',
         idx(P4, 'antivirus → Administrar la'), 60)]))

    # --- 13. los numeros que se usan dentro de MAS
    F.append(('figura-13.png', P4, [], [
        ('Dentro de MAS escribe el 2\npara activar Office',
         idx(P4, '2 = activar Office'), 25),
        ('Escribe 1 para abrir MAS',
         idx(P4, 'Sí, abrir MAS'), 40)]))

    # --- 14. comprobar la licencia
    F.append(('figura-14.png', P5, [
        (1, idx(P5, '  Producto'), idx(P5, '  Arquitectura'), 2, 71)], [
        ('Que version tienes',
         idx(P5, '  Producto'), 55),
        ('SI PONE ---LICENSED---\nesta activado',
         idx(P5, 'LICENSE STATUS'), 45)]))

    # --- 15. la opcion 7, con los numeros al reves
    F.append(('figura-15.png', P7, [
        (1, idx(P7, 'aquí el 1 es CANCELAR'), idx(P7, 'aquí el 1 es CANCELAR'), 2, 71)], [
        ('OJO: aqui el 1 CANCELA',
         idx(P7, 'No, cancelar y volver'), 40),
        ('Solo el 2 borra Office',
         idx(P7, 'Sí, borrar Office de este'), 40)]))

    # --- 16. el error de permisos
    F.append(('figura-16.png', P8, [
        (1, idx(P8, 'FALTAN PERMISOS'), idx(P8, 'Después vuelve a abrir'), 2, 71)], [
        ('El programa te dice\nexactamente que hacer',
         idx(P8, 'y elige  "Ejecutar como'), 60)]))

    return F


RECORTES = {          # figura -> (texto donde empieza, texto donde acaba)
    'figura-01.png': ('INSTITUTO SUPERIOR', 'Revisión del equipo'),
    'figura-02.png': ('Revisión del equipo', '   INSTALAR OFFICE'),
    'figura-03.png': ('   INSTALAR OFFICE', '   OTRAS OPCIONES'),
    'figura-04.png': ('   OTRAS OPCIONES', 'Escribe el número de la opción'),
    'figura-05.png': ('   OTRAS OPCIONES', None),
    'figura-06.png': ('Resumen de lo que se va', 'NO CIERRES ESTA VENTANA', -2),
    'figura-07.png': ('NO CIERRES ESTA VENTANA', '¿Quieres instalarlo ahora?'),
    'figura-08.png': ('¿Quieres instalarlo ahora?', None),
    'figura-09.png': ('Descargando el instalador oficial', 'Preparando la configuración'),
    'figura-11.png': ('OFFICE INSTALADO CORRECTAMENTE', None),
    'figura-12.png': ('Activar Office con MAS', 'Se abrirá el menú de MAS'),
    'figura-13.png': ('Se abrirá el menú de MAS', None),
}

if __name__ == '__main__':
    check()
    base = '/mnt/disco1tb/diego/office_script/capturas/'
    for n, p in PANTALLAS:
        if n.startswith('PS') or n.startswith('MAS'):
            render(p, f'{base}pantalla-{n.lower()}.png',
                   titulo_ventana='Administrador: Windows PowerShell', fondo=AZUL_PS)
        else:
            render(p, f'{base}pantalla-{n.lower()}.png')
    figs = figuras()          # si una ancla desaparece, revienta aqui
    print('CHECK anclas de figura: OK  (%d figuras)' % len(figs))
    for nombre, pantalla, marcas, flechas in figs:
        if nombre.startswith('figura-mas'):
            print(' ->', render(pantalla, base + nombre, marcas, flechas,
                                'Administrador: Microsoft Activation Scripts 3.12', AZUL_PS))
            continue
        if nombre.startswith('figura-ps'):
            print(' ->', render(pantalla, base + nombre, marcas, flechas,
                                'Administrador: Windows PowerShell', AZUL_PS))
            continue
        if nombre in RECORTES:
            r = RECORTES[nombre]
            ini, fin, ajuste = (r + (0,))[:3] if len(r) == 2 else r
            desde = max(0, idx(pantalla, ini) - 1)
            hasta = (idx(pantalla, fin) + ajuste if fin else len(pantalla))
            # tras recortar, el recuadro sobra: la figura YA es esa zona
            pantalla, marcas, flechas = recortar(pantalla, [], flechas, desde, hasta)
        print(' ->', render(pantalla, base + nombre, marcas, flechas))
