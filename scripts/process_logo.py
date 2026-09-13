"""Convierte el logo real (fondo negro, marca blanca) subido por el cliente
en marcas de agua con fondo transparente, reutilizables sobre cualquier
sección clara u oscura del sitio, más los iconos de favicon/manifest y la
imagen Open Graph — todo a partir del logo REAL, no del emblema inventado
que se generaba antes con gen_assets.py (ese script queda obsoleto en
cuanto a la marca, pero se conserva por si hace falta regenerar solo el
fondo del OG image)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC = "assets/img/source/logo-original.jpg"

TINTA = (23, 19, 13)        # --tinta (nuevo, sacado del negro real del logo)
PAPEL = (244, 238, 223)     # --papel (crema del menú real)
HOJA = (183, 146, 58)       # --sendero (dorado de la hoja/ilustración de bellotas)


def extract_mark():
    im = Image.open(SRC).convert("RGB")
    w, h = im.size
    arr = np.array(im.convert("L")).astype(np.float32)

    # Recorta las barras de letterbox (negro puro, media de fila ~0) y deja
    # un margen de seguridad.
    row_means = arr.mean(axis=1)
    top = 0
    while top < h and row_means[top] < 3:
        top += 1
    bottom = h - 1
    while bottom > 0 and row_means[bottom] < 3:
        bottom -= 1
    pad = 6
    top = max(0, top - pad)
    bottom = min(h - 1, bottom + pad)
    im = im.crop((0, top, w, bottom + 1))
    arr = arr[top : bottom + 1, :]

    # Fondo real ~ nivel 20/255 (no negro puro) — usa eso como pie de la
    # rampa de alpha para que el fondo quede totalmente transparente y el
    # trazo blanco quede opaco, con anti-aliasing suave en el borde.
    bg_level, white_level = 28.0, 130.0
    alpha = np.clip((arr - bg_level) / (white_level - bg_level), 0, 1) * 255
    alpha = alpha.astype(np.uint8)

    mark_white = Image.new("RGBA", im.size, (255, 255, 255, 0))
    mark_white.putalpha(Image.fromarray(alpha))
    # el propio color ya es blanco puro (255,255,255) constante, con el
    # canal alfa llevando toda la forma — asegurarlo explícitamente:
    solid_white = Image.new("RGBA", im.size, (255, 255, 255, 255))
    mark_white = Image.composite(solid_white, Image.new("RGBA", im.size, (255, 255, 255, 0)), Image.fromarray(alpha))

    # Recorte cuadrado centrado en el contenido real (no en el lienzo
    # completo, que tiene aire de sobra a los lados).
    bbox = mark_white.getbbox()
    mark_white = mark_white.crop(bbox)

    return mark_white


def square_pad(img, pad_frac=0.14, size=None):
    w, h = img.size
    side = max(w, h)
    pad = int(side * pad_frac)
    canvas = Image.new("RGBA", (side + pad * 2, side + pad * 2), (0, 0, 0, 0))
    canvas.paste(img, ((side + pad * 2 - w) // 2, (side + pad * 2 - h) // 2), img)
    if size:
        canvas = canvas.resize((size, size), Image.LANCZOS)
    return canvas


def recolor(img, rgb):
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    solid = Image.new("RGBA", img.size, rgb + (255,))
    out = Image.composite(solid, out, img.split()[3])
    return out


if __name__ == "__main__":
    import os

    os.makedirs("assets/img/logo", exist_ok=True)

    mark = extract_mark()
    mark_sq = square_pad(mark, pad_frac=0.16)

    # Marca blanca sobre transparente (para fondos oscuros: hero, footer,
    # overlay-nav) y marca en tinta sobre transparente (para fondos claros:
    # cabecera, fondo de página).
    white_mark = mark_sq
    white_mark.save("assets/img/logo/mark-white.png")

    ink_mark = recolor(mark_sq, TINTA)
    ink_mark.save("assets/img/logo/mark-ink.png")

    # Favicons / iconos de "añadir a inicio": la marca en tinta sobre un
    # círculo de papel (crema), igual que webs hermanas pero con la marca
    # real en vez de un emblema inventado.
    def make_icon(size, out_path):
        S = size * 4
        base = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        d = ImageDraw.Draw(base)
        d.ellipse([0, 0, S, S], fill=PAPEL + (255,))
        m = ink_mark.resize((int(S * 0.66), int(S * 0.66)), Image.LANCZOS)
        base.alpha_composite(m, ((S - m.width) // 2, (S - m.height) // 2 - int(S * 0.02)))
        base = base.resize((size, size), Image.LANCZOS)
        base.save(out_path)
        print("wrote", out_path, size)

    make_icon(96, "assets/img/logo/icon-96.png")
    make_icon(180, "assets/img/logo/icon-180.png")
    make_icon(192, "assets/img/logo/icon-192.png")
    make_icon(512, "assets/img/logo/icon-512.png")

    # Imagen Open Graph con la marca real sobre el fondo tinta/crema del
    # sitio y el sendero de veneras como eco del hero.
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), TINTA)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        r = int(TINTA[0] * (1 - t) + 10 * t)
        g = int(TINTA[1] * (1 - t) + 8 * t)
        b = int(TINTA[2] * (1 - t) + 6 * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))

    path_pts = [(-40, 520), (260, 460), (520, 500), (760, 380), (1020, 300), (1280, 260)]
    d.line(path_pts, fill=HOJA, width=6, joint="curve")
    for i in (1, 3):
        x, y = path_pts[i]
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=PAPEL)

    mark_og = white_mark.resize((190, int(190 * white_mark.height / white_mark.width)), Image.LANCZOS)
    img.paste(mark_og, (78, 70), mark_og)

    font_title = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 62)
    d.text((80, 300), "O Carballo Tapería", font=font_title, fill=PAPEL)
    font_sub = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 28)
    d.text((82, 380), "Tapería en Sigüeiro, última etapa del Camino Inglés", font=font_sub, fill=(214, 204, 186))

    img.save("assets/img/web/og-image.jpg", quality=88)
    print("wrote assets/img/web/og-image.jpg")
