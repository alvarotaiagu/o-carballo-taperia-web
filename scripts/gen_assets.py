"""Genera el emblema de marca y la imagen Open Graph para O Carballo Tapería.
No hay logo real del negocio disponible (Instagram/Facebook bloquean el
scraping y no hay ficha con imagen descargable), así que se crea un emblema
propio (no una foto, no un icono de terceros): una hoja de roble (por el
nombre real del negocio, "carballo" = roble en gallego) enlazada con una
venera estilizada (símbolo real y público de señalización del Camino de
Santiago; el negocio está confirmado en el trazado del Camino Inglés). Son
formas geométricas simples propias de un emblema de marca, no una escena
ilustrada.
"""
import math
from PIL import Image, ImageDraw, ImageFont

MARCO = (31, 63, 92)         # --marco (azul de señal de Camino)
MARCO_HONDO = (20, 41, 60)   # --marco-hondo
SENDERO = (217, 162, 27)     # --sendero (amarillo de flecha de Camino)
ROBLE = (139, 98, 57)        # --roble
FRAGA = (70, 89, 46)         # --fraga
PAPEL = (246, 240, 228)      # --papel
TINTA = (36, 28, 21)         # --tinta

FONT_BOLD = "C:/Windows/Fonts/georgiab.ttf"


def draw_oak_leaf(d, cx, cy, size, fill):
    """Hoja de roble simplificada: pares de lóbulos redondeados (círculos
    solapados) a lo largo de un eje central, más un ápice — silueta plana
    típica de icono de hoja, no una ilustración detallada."""
    lobe_rows = [
        (0.62, 0.30),  # (posición y desde el centro hacia abajo, radio)
        (0.30, 0.34),
        (-0.06, 0.36),
    ]
    for y_t, radius in lobe_rows:
        y = cy - size * y_t
        rx = size * radius
        d.ellipse([cx - rx * 0.95, y - rx, cx - rx * 0.05, y + rx], fill=fill)
        d.ellipse([cx + rx * 0.05, y - rx, cx + rx * 0.95, y + rx], fill=fill)
    # base y ápice para redondear el contorno general
    d.ellipse([cx - size * 0.22, cy + size * 0.32, cx + size * 0.22, cy + size * 0.72], fill=fill)
    d.ellipse([cx - size * 0.16, cy - size * 1.0, cx + size * 0.16, cy - size * 0.6], fill=fill)
    tip = (cx, cy - size * 1.02)
    base = (cx, cy + size * 0.7)
    d.line([tip, base], fill=TINTA, width=max(1, int(size * 0.05)))


def draw_shell(d, cx, cy, size, fill):
    """Venera estilizada: abanico de líneas desde un punto sobre un arco inferior."""
    rays = 7
    r = size * 0.62
    start_angle = math.radians(200)
    end_angle = math.radians(340)
    base_y = cy + size * 0.18
    d.pieslice([cx - r, base_y - r, cx + r, base_y + r], 200, 340, fill=fill)
    for i in range(rays):
        a = start_angle + (end_angle - start_angle) * (i / (rays - 1))
        x2 = cx + r * math.cos(a)
        y2 = base_y + r * math.sin(a)
        d.line([(cx, base_y), (x2, y2)], fill=TINTA, width=max(1, int(size * 0.03)))
    d.arc([cx - r, base_y - r, cx + r, base_y + r], 200, 340, fill=TINTA, width=max(1, int(size * 0.035)))


def make_icon(size, out_path):
    scale = 4
    S = size * scale
    base = Image.new("RGBA", (S, S), (0, 0, 0, 0))

    pad = int(S * 0.04)
    circle_mask = Image.new("L", (S, S), 0)
    cmd = ImageDraw.Draw(circle_mask)
    cmd.ellipse([pad, pad, S - pad, S - pad], fill=255)

    layer = Image.new("RGBA", (S, S), MARCO + (255,))
    ld = ImageDraw.Draw(layer)
    ld.rectangle([0, int(S * 0.6), S, S], fill=MARCO_HONDO + (255,))

    draw_shell(ld, S * 0.5, S * 0.66, S * 0.32, SENDERO)
    draw_oak_leaf(ld, S * 0.5, S * 0.34, S * 0.15, PAPEL)

    base.paste(layer, (0, 0), circle_mask)
    img = base.resize((size, size), Image.LANCZOS)
    img.save(out_path)
    print("wrote", out_path, size)


def make_og_image(out_path):
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), MARCO_HONDO)
    d = ImageDraw.Draw(img)

    for y in range(H):
        t = y / H
        r = int(MARCO[0] * (1 - t) + MARCO_HONDO[0] * t)
        g = int(MARCO[1] * (1 - t) + MARCO_HONDO[1] * t)
        b = int(MARCO[2] * (1 - t) + MARCO_HONDO[2] * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))

    # Línea de camino con marcas de flecha, eco abstracto del hero — sin
    # dibujar ninguna escena o persona.
    path_pts = [(-40, 520), (260, 460), (520, 500), (760, 380), (1020, 300), (1280, 260)]
    d.line(path_pts, fill=SENDERO, width=6, joint="curve")
    for i in (1, 3):
        x, y = path_pts[i]
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=PAPEL)

    cx, cy, r = 150, 150, 78
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PAPEL)
    draw_shell(d, cx, cy + 20, 42, SENDERO)
    draw_oak_leaf(d, cx, cy - 26, 20, MARCO)

    font_title = ImageFont.truetype(FONT_BOLD, 68)
    d.text((80, 260), "O Carballo Tapería", font=font_title, fill=PAPEL)

    font_sub = ImageFont.truetype(FONT_BOLD, 28)
    d.text((82, 348), "Tapería en Sigüeiro, última etapa del Camino Inglés", font=font_sub, fill=(224, 214, 196))

    img.save(out_path, quality=88)
    print("wrote", out_path)


if __name__ == "__main__":
    import os
    base = "assets/img/logo"
    os.makedirs(base, exist_ok=True)
    make_icon(96, f"{base}/icon-96.png")
    make_icon(180, f"{base}/icon-180.png")
    make_icon(192, f"{base}/icon-192.png")
    make_icon(512, f"{base}/icon-512.png")
    os.makedirs("assets/img/web", exist_ok=True)
    make_og_image("assets/img/web/og-image.jpg")
