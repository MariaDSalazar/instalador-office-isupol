#!/usr/bin/env python3
"""Genera las figuras que no salen de la consola:
  figura-web1.png  la pagina del repositorio (captura REAL + marco de navegador)
  figura-win1.png  el menu Inicio buscando PowerShell   (recreacion)
  figura-win2.png  el aviso de permisos de Windows (UAC) (recreacion)

La captura de GitHub es autentica (Chrome headless sobre la URL real). El marco
del navegador y las dos pantallas de Windows son recreaciones dibujadas: este
equipo es Linux y no puede capturar Windows de verdad.
"""
import math, subprocess, pathlib
from PIL import Image, ImageDraw, ImageFont

BASE = pathlib.Path('/mnt/disco1tb/diego/office_script/capturas')
URL = 'https://github.com/MariaDSalazar/instalador-office-isupol'
ROJO = '#E01B24'
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FM = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
fnt = lambda t, s: ImageFont.truetype({'r': F, 'b': FB, 'm': FM}[t], s)


# ---------------------------------------------------------------- utiles
def flecha(d, x1, y1, x2, y2, w=5):
    d.line([x1, y1, x2, y2], fill=ROJO, width=w)
    a = math.atan2(y2 - y1, x2 - x1)
    for s in (1, -1):
        b = a + s * math.radians(155)
        d.line([x2, y2, x2 + 22 * math.cos(b), y2 + 22 * math.sin(b)], fill=ROJO, width=w)


def circulo(d, x, y, n, r=26):
    d.ellipse([x - r, y - r, x + r, y + r], fill=ROJO)
    f = fnt('b', 32)
    w = d.textlength(str(n), font=f)
    d.text((x - w / 2, y - 21), str(n), font=f, fill='white')


def marco_navegador(ancho, alto_contenido, url):
    """Barra de titulo + pestana + barra de direcciones de un navegador."""
    ALTO = 96
    im = Image.new('RGB', (ancho, ALTO + alto_contenido), '#202124')
    d = ImageDraw.Draw(im)
    # pestana
    d.rounded_rectangle([12, 8, 330, 44], radius=8, fill='#35363a')
    d.ellipse([24, 18, 40, 34], fill='#f0f0f0')
    d.text((50, 18), 'MariaDSalazar/instalador-of…', font=fnt('r', 15), fill='#e8eaed')
    # barra de direcciones
    d.rounded_rectangle([92, 54, ancho - 60, 88], radius=17, fill='#35363a')
    d.text((108, 63), '⚿', font=fnt('r', 16), fill='#9aa0a6')
    d.text((134, 62), url, font=fnt('r', 17), fill='#e8eaed')
    return im, ALTO


# ------------------------------------------------- 1. pagina del repo
def figura_web():
    png = pathlib.Path('/tmp/github-full.png')
    if not png.exists():
        subprocess.run(['google-chrome', '--headless', '--disable-gpu', '--no-sandbox',
                        '--hide-scrollbars', '--window-size=1440,3400',
                        f'--screenshot={png}', '--virtual-time-budget=15000', URL],
                       capture_output=True, timeout=180)
    full = Image.open(png)
    banda = full.crop((60, 2248, 1040, 2380))      # "Forma 1" + el comando
    banda = banda.resize((int(banda.width * 1.35), int(banda.height * 1.35)))

    ancho = banda.width + 120
    im, top = marco_navegador(ancho, banda.height + 90, URL)
    im.paste(banda, (60, top + 40))
    d = ImageDraw.Draw(im)

    # 1 -> barra de direcciones
    circulo(d, 46, 71, 1)
    d.rounded_rectangle([92, 54, ancho - 60, 88], radius=17, outline=ROJO, width=4)
    # 2 -> el recuadro del comando
    y_cmd = top + 40 + int(banda.height * 0.72)
    d.rounded_rectangle([74, y_cmd - 28, 60 + banda.width - 6, y_cmd + 28],
                        radius=7, outline=ROJO, width=4)
    circulo(d, 46, y_cmd, 2)
    # flecha al boton de copiar (el icono al final de la linea)
    bx = 60 + banda.width - 46
    d.text((bx - 430, y_cmd + 62), 'el botoncito de copiar', font=fnt('b', 21), fill=ROJO)
    flecha(d, bx - 150, y_cmd + 66, bx - 4, y_cmd + 20)
    im.save(BASE / 'figura-web1.png')
    return 'figura-web1.png', im.size


# ------------------------------------- 2. menu Inicio buscando PowerShell
def figura_inicio():
    W, H = 1180, 700
    im = Image.new('RGB', (W, H), '#1f1f1f')
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([20, 20, W - 20, H - 20], radius=14, fill='#2b2b2b')
    # caja de busqueda
    d.rounded_rectangle([48, 48, W - 48, 100], radius=8, fill='#3a3a3a')
    d.ellipse([72, 64, 90, 82], outline='#bbb', width=2)          # lupa
    d.line([88, 80, 96, 88], fill='#bbb', width=2)
    d.text((108, 62), 'PowerShell', font=fnt('r', 22), fill='#fff')
    d.text((48, 124), 'Mejor coincidencia', font=fnt('b', 16), fill='#9ecbff')
    # resultado seleccionado
    d.rounded_rectangle([48, 152, 600, 232], radius=8, fill='#0f4a8a')
    d.rounded_rectangle([70, 170, 114, 214], radius=6, fill='#012456')
    d.text((80, 180), '>_', font=fnt('m', 22), fill='#fff')
    d.text((134, 168), 'Windows PowerShell', font=fnt('b', 21), fill='#fff')
    d.text((134, 196), 'Aplicación', font=fnt('r', 16), fill='#cfd8e3')
    # panel derecho con las acciones
    d.line([640, 152, 640, 560], fill='#454545', width=2)
    d.rounded_rectangle([680, 160, 724, 204], radius=6, fill='#012456')
    d.text((690, 170), '>_', font=fnt('m', 22), fill='#fff')
    d.text((744, 162), 'Windows PowerShell', font=fnt('b', 20), fill='#fff')
    d.text((744, 190), 'Aplicación', font=fnt('r', 15), fill='#b8b8b8')
    acciones = ['Abrir', 'Ejecutar como administrador',
                'Abrir la ubicación del archivo', 'Anclar a Inicio',
                'Anclar a la barra de tareas']
    for i, a in enumerate(acciones):
        y = 256 + i * 46
        neg = (i == 1)
        if neg:                                                    # escudo del UAC
            d.polygon([(714, y + 2), (726, y - 3), (738, y + 2), (738, y + 12),
                       (726, y + 22), (714, y + 12)], fill='#9ecbff')
        else:
            d.text((716, y), '▷' if i == 0 else '·', font=fnt('r', 17), fill='#9a9a9a')
        d.text((748, y - 2), a, font=fnt('b' if neg else 'r', 19),
               fill='#fff' if neg else '#d8d8d8')
    d.text((48, 620), 'Escribe aquí para buscar', font=fnt('r', 17), fill='#8a8a8a')

    # anotaciones
    circulo(d, 26, 74, 1)
    d.rounded_rectangle([48, 48, W - 48, 100], radius=8, outline=ROJO, width=4)
    circulo(d, 660, 300, 2)
    d.rounded_rectangle([700, 274, W - 40, 324], radius=8, outline=ROJO, width=4)
    d.text((60, 300), 'ESTA es la opcion correcta:', font=fnt('b', 22), fill=ROJO)
    d.text((60, 330), '"Ejecutar como administrador",', font=fnt('b', 22), fill=ROJO)
    d.text((60, 360), 'NO la de "Abrir"', font=fnt('b', 22), fill=ROJO)
    flecha(d, 470, 320, 690, 300)
    im.save(BASE / 'figura-win1.png')
    return 'figura-win1.png', im.size


# ------------------------------------------- 3. el aviso de permisos (UAC)
def figura_uac():
    W, H = 900, 560
    im = Image.new('RGB', (W, H), '#0a0a0a')
    d = ImageDraw.Draw(im)
    dlg = [140, 60, W - 140, H - 90]
    d.rounded_rectangle(dlg, radius=10, fill='#202020')
    d.rounded_rectangle([dlg[0], dlg[1], dlg[2], dlg[1] + 74], radius=10, fill='#0f4a8a')
    d.rectangle([dlg[0], dlg[1] + 50, dlg[2], dlg[1] + 74], fill='#0f4a8a')
    d.text((dlg[0] + 28, dlg[1] + 24), 'Control de cuentas de usuario',
           font=fnt('b', 21), fill='#fff')
    d.text((dlg[0] + 28, dlg[1] + 104), '¿Quieres permitir que esta aplicación',
           font=fnt('b', 24), fill='#fff')
    d.text((dlg[0] + 28, dlg[1] + 136), 'haga cambios en el dispositivo?',
           font=fnt('b', 24), fill='#fff')
    d.rounded_rectangle([dlg[0] + 28, dlg[1] + 190, dlg[0] + 84, dlg[1] + 246],
                        radius=6, fill='#012456')
    d.text((dlg[0] + 40, dlg[1] + 204), '>_', font=fnt('m', 26), fill='#fff')
    d.text((dlg[0] + 104, dlg[1] + 192), 'Windows PowerShell', font=fnt('b', 19), fill='#fff')
    d.text((dlg[0] + 104, dlg[1] + 220), 'Editor comprobado: Microsoft Windows',
           font=fnt('r', 16), fill='#b8b8b8')
    d.text((dlg[0] + 28, dlg[1] + 268), 'Mostrar más detalles', font=fnt('r', 17), fill='#9ecbff')
    # botones
    by = dlg[3] - 74
    d.rounded_rectangle([dlg[2] - 330, by, dlg[2] - 190, by + 50], radius=5,
                        fill='#2d5f9a', outline='#5b9bd5', width=2)
    d.text((dlg[2] - 285, by + 13), 'Sí', font=fnt('b', 22), fill='#fff')
    d.rounded_rectangle([dlg[2] - 170, by, dlg[2] - 30, by + 50], radius=5,
                        fill='#3a3a3a', outline='#5a5a5a', width=2)
    d.text((dlg[2] - 137, by + 13), 'No', font=fnt('r', 22), fill='#e8e8e8')

    # anotacion
    d.rounded_rectangle([dlg[2] - 334, by - 4, dlg[2] - 186, by + 54],
                        radius=6, outline=ROJO, width=4)
    d.text((60, by + 96), 'Haz clic en Si', font=fnt('b', 24), fill=ROJO)
    flecha(d, 250, by + 100, dlg[2] - 262, by + 60)
    im.save(BASE / 'figura-win2.png')
    return 'figura-win2.png', im.size


if __name__ == '__main__':
    for f in (figura_web, figura_inicio, figura_uac):
        print(' ->', *f())
