"""Descarga y procesa las fotografías de ambiente con licencia libre
(Unsplash License, uso comercial sin permiso) usadas en el sitio, ya que el
negocio no facilitó fotografía propia salvo la carta y el logo. Genera
tamaños responsive (grande/pequeño) + una miniatura LQIP borrosa real (no
base64 incrustado a mano) para el patrón de blur-up ya usado en las webs
hermanas (ver webtest/js/main.js initLqipReveal).

Procedencia de cada foto (Unsplash, licencia libre — ver README):
- fraga-robles: "A sun-dappled path lined with old oak trees" variant —
  en realidad se usó la foto de David Gabrić (bosque de robles en otoño,
  fotografía de ambiente, no es una foto real del Camino en Sigüeiro).
- cocina-tapas: Nacho Carretero Molero — albóndigas y tapas.
- carta-arroces: Armando Brenlha — paella de marisco.
- carta-delmar: fotografía de gambas a la plancha.
- carta-tostas: Nacho Carretero Molero — tostas variadas.
"""
import os
import urllib.request
from PIL import Image, ImageFilter

PHOTOS = {
    "fraga-robles": "https://images.unsplash.com/photo-1604400557709-fdcfba8ace1a",
    "cocina-tapas": "https://images.unsplash.com/photo-1565599837634-134bc3aadce8",
    "carta-arroces": "https://images.unsplash.com/photo-1630175860333-5131bda75071",
    "carta-delmar": "https://images.unsplash.com/photo-1723325697529-6e2679650b39",
    "carta-tostas": "https://images.unsplash.com/photo-1649886188423-abc62ed967d6",
}

OUT = "assets/img/photos"
os.makedirs(OUT, exist_ok=True)


def fetch(url, w, q=80):
    req = urllib.request.Request(f"{url}?w={w}&q={q}&fm=jpg&fit=crop", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as r:
        return r.read()


for name, url in PHOTOS.items():
    large_bytes = fetch(url, 1400, 82)
    small_bytes = fetch(url, 800, 78)
    large_path = f"{OUT}/{name}-1400.jpg"
    small_path = f"{OUT}/{name}-800.jpg"
    with open(large_path, "wb") as f:
        f.write(large_bytes)
    with open(small_path, "wb") as f:
        f.write(small_bytes)

    # LQIP: tiny real blurred jpg, not embedded base64.
    im = Image.open(small_path).convert("RGB")
    tiny = im.resize((32, round(32 * im.height / im.width)), Image.LANCZOS)
    tiny = tiny.filter(ImageFilter.GaussianBlur(2))
    lqip_path = f"{OUT}/{name}-lqip.jpg"
    tiny.save(lqip_path, quality=40)

    w, h = Image.open(large_path).size
    print(name, "large", w, h, "->", large_path, small_path, lqip_path)
