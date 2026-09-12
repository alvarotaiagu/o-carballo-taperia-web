# O Carballo Tapería — landing

Sitio estático (HTML/CSS/JS, sin build), mismo *toolkit* técnico que
[melao-carballo-web](https://github.com/alvarotaiagu/melao-carballo-web),
[taberna-do-rio-carballo-web](https://github.com/alvarotaiagu/taberna-do-rio-carballo-web)
y [o-logradouro-carballo-web](https://github.com/alvarotaiagu/o-logradouro-carballo-web)
(GSAP + ScrollTrigger, Lenis) pero con su **propia estructura de página y su
propia técnica de hero** — ver "Quinta familia estructural" más abajo. Abrir
`index.html` con un servidor estático cualquiera (por ejemplo
`python -m http.server`) — no funciona bien con `file://` porque las fuentes
y `js/main.js` necesitan HTTP.

## Quinta familia estructural del workspace

Este workspace usa cada web como plantilla reutilizable para vender a
futuros clientes, así que cada sitio debe leerse como una plantilla
distinta, no como un reskin. Antes de escribir una sola línea se revisó la
estructura de las cuatro webs hermanas (Melao, Marabú, A Taberna do Rio,
O Logradouro) para no repetir ni el orden de secciones ni la técnica de
hero de ninguna. El hilo conductor elegido aquí es real y verificable: el
negocio está confirmado en el trazado del **Camino Inglés** (turismo.gal),
en su última etapa antes de Santiago — así que toda la identidad se apoya
en esa geografía real, no en un concepto inventado:

- **Hero: sendero de señalización** (`js/scene-camino.js`): un camino
  discontinuo que fluye por el canvas con veneras y flechas — símbolos
  públicos y reales de señalización del Camino de Santiago, no clip-art —
  pulsando en sus paradas y un punto de luz que recorre la ruta. Ninguna
  web hermana usa esta técnica: Melao usa un shader de blobs, A Taberna do
  Rio y O Logradouro usan iconos de platos orbitando (con y sin acabado
  "gooey"), Marabú usa partículas ambiente.
- **Contador de kilómetros** (`.km-counter`): un widget fijo que cuenta
  hacia atrás de 16 a 0 según el progreso de scroll de toda la página —
  los dieciséis kilómetros reales de la última etapa del Camino Inglés
  entre Sigüeiro y la catedral. Ninguna web hermana tiene un elemento de
  navegación equivalente.
- **Menú a pantalla completa** (`#overlay-nav`) en vez del nav de píldoras
  de Melao, la barra lateral de puntos de A Taberna do Rio/O Logradouro, o
  el menú desplegable simple de Marabú — secciones numeradas como paradas
  de un itinerario.
- **"La última etapa"** (`#etapa`): una franja de paradas con línea
  discontinua y desnivel alterno (perfil de sendero) que traduce la
  distancia real Sigüeiro→Santiago (Ponte do Tambre, Fraga Encantada) en
  vez de una franja horaria como "momentos" de O Logradouro.
- **"La carta"** (`#carta`): tarjetas "sello" con borde discontinuo tipo
  credencial de peregrino y el precio como sello circular en la esquina —
  con **precios reales** de la carta consultada en TripAdvisor, a
  diferencia del foco+índice sin precios de O Logradouro. Deliberadamente
  distinto también de la hoja de precios de A Taberna do Rio y del grid de
  fotos de Melao.
- **"Reconocimientos"** (`#reconocimientos`): sin cifra de valoración —
  TripAdvisor no mostraba reseñas verificadas propias en el momento de la
  consulta (12-09-2026) — así que el foco es el sello real de Travellers'
  Choice, no un número inventado ni un anillo de valoración como en A
  Taberna do Rio/O Logradouro.

Validado con Playwright (Chromium local) en desktop/mobile, con
`reducedMotion: 'reduce'`, con `javaScriptEnabled: false` y con scroll real
completo (rueda del ratón simulada, no solo `scrollIntoView`, ya que una
captura estática con salto instantáneo no dispara los `ScrollTrigger`):
0 errores de consola y 0 requests fallidas en los cuatro modos.

## Dirección de arte

- **Idea visual:** una tapería en Sigüeiro (Oroso) que es, literalmente, la
  última parada antes de que el Camino Inglés entre en Santiago — de ahí el
  titular "El descanso justo antes de Santiago."
- **Paleta:** el negocio **no tiene logo ni manual de marca disponible**
  (Instagram/Facebook bloquean el scraping automatizado). En vez de
  inventar un color al azar, la paleta se apoya en dos fuentes honestas y
  reales: la madera del roble (**"carballo" = roble en gallego**, el propio
  nombre del negocio: `--roble` `#8B6239`) y la señalización pública del
  Camino de Santiago — el azul de las señales direccionales (`--marco`
  `#1F3F5C`) y el amarillo de las flechas/veneras (`--sendero` `#D9A21B`) —
  ya que el negocio está confirmado en el trazado del Camino Inglés. Un
  verde de carballeira/fraga (`--fraga` `#46592E`) completa la paleta.
  Deliberadamente distinta de: coral/cielo/lima (Melao), verde
  río/madera/dorado (A Taberna do Rio), piedra/barro/vino/oliva (O
  Logradouro). Ver `css/style.css`, bloque `:root`.
- **Tipografía:** Spectral (serif con itálica expresiva) + Manrope (texto e
  interfaz) — pareja propia, distinta de Fraunces+Work Sans (O Logradouro)
  y Bitter+Inter (Melao/A Taberna do Rio).
- **Logo:** sin logo real facilitado. Se creó un emblema propio
  (`scripts/gen_assets.py`): una hoja de roble estilizada sobre una venera
  — el nombre del negocio y el símbolo real del Camino, no dos formas
  inventadas al azar. **No es un logo real del negocio** — si el dueño
  aporta uno propio, sustituir estos archivos.
- **Fotografía / ilustración — IMPORTANTE:** el negocio no facilitó banco
  de fotos propio y esta sesión no tuvo forma de obtener fotos reales
  (Instagram/Facebook bloquean el scraping de imágenes). Igual que en
  O Logradouro, el sitio es **deliberadamente fotográfico-cero e
  ilustración-cero**: toda la identidad visual corre a cargo de la
  tipografía, los iconos de interfaz (Iconify Solar/MDI/Simple Icons), los
  gráficos de datos (franja de paradas, contador de kilómetros, sello de
  reconocimiento) y la escena de canvas del hero (símbolos de señalización
  con motion, no una fotografía).
  **Antes de enseñar la web al dueño, lo ideal es conseguir fotos reales**
  del local y 2–3 platos para añadir una sección de imágenes — la
  estructura del sitio no depende de ellas.
- **Motion:** GSAP + ScrollTrigger para las revelaciones por sección, Lenis
  como motor de scroll suave. Todo el motion es opcional: si el CDN de
  GSAP/Lenis falla, el sitio se degrada con limpieza — menú, horario en
  vivo, mapa y WhatsApp siguen funcionando sin errores de consola.
- **Icons:** Iconify — Solar para símbolos de interfaz, MDI para
  Instagram/Facebook, `ri` para el glifo de WhatsApp y
  `simple-icons:tripadvisor` para el sello real de TripAdvisor.
- **Skill de diseño usada:** `build-awwwards-quality-sites`, con dirección
  de arte propia (paleta, tipografía, contenido y estructura) para este
  negocio.

## Contenido real vs. pendiente

**Confirmado y usado tal cual** (TripAdvisor, turismo.gal y
paxinasgalegas.es, consultados 12-09-2026):
- Nombre (O Carballo Tapería / Tapería O Carballo), dirección (Avenida da
  Grabanxa, 29, Sigüeiro, 15888 Oroso, A Coruña), confirmado en el trazado
  del Camino Inglés (parroquia de Oroso — San Martiño, lugar de Sigüeiro).
- Teléfono (690 02 02 86, coincidente en turismo.gal y en búsqueda
  independiente) y email (manuelfrala@gmail.com, ficha oficial de
  turismo.gal).
- Horario: miércoles y jueves 9:00–23:00, viernes 9:00–1:00, sábado
  10:00–1:00, domingo 10:00–23:00, lunes y martes cerrado; cocina
  13:00–16:00 y 21:00–23:30 — coincidente entre la captura de horario
  aportada y la ficha de TripAdvisor.
- Carta y precios reales de TripAdvisor: Ensalada O Carballo (14,50 €),
  Ensalada templada de rulo de cabra (15,50 €), Ensalada de ventresca y
  queso de Arzúa (16,50 €), Croquetas de jamón ibérico (12,50 €), Secreto
  ibérico con patatas (18,50 €), Hamburguesa O Carballo (13,50 €). El plato
  "Croca de Vaca Fileteada" (21,50 €) del OCR de TripAdvisor se normalizó a
  "Chuleta de vaca fileteada" por ser la lectura con sentido más plausible
  del nombre del plato — el precio es el real y verificado.
- Reconocimiento Travellers' Choice de TripAdvisor (visible en la ficha
  consultada).
- Distancia real Sigüeiro→Santiago (última etapa del Camino Inglés, ~16
  km, cruzando el Ponte do Tambre y la Fraga Encantada) — fuentes públicas
  de operadores del Camino Inglés (caminoingles.gal, Galiwonders, etc.).
  Las distancias intermedias de Ponte do Tambre y Fraga Encantada en la
  franja `#etapa` (≈11 km y ≈5 km) son una interpolación aproximada sobre
  el total real de 16 km, no una medición propia verificada punto a punto.
- Cuenta de Instagram `@ocarballotaperia` y página de Facebook
  "O Carballo Taperia" (URLs facilitadas directamente por el cliente).

**⚠️ Pendiente / decisiones tomadas por mi cuenta — revisar antes de
enseñar la web:**
- **Fotos reales** (ver "Fotografía" arriba) — es el ajuste pendiente más
  importante.
- **Valoración/reseñas**: TripAdvisor mostraba 0 reseñas en el momento de
  la consulta, mientras que un directorio de terceros (paxinasgalegas.es)
  citaba "5,0 (100+)" sin poder verificarse contra la propia ficha de
  TripAdvisor — por eso la web **no muestra ninguna cifra de valoración**,
  solo el sello real de Travellers' Choice. Si el negocio confirma una
  valoración de Google verificable, se puede añadir siguiendo el patrón de
  O Logradouro/A Taberna do Rio.
- **WhatsApp**: se asume que 690 02 02 86 (móvil español) tiene WhatsApp
  activo, igual que se asumió en las webs hermanas — falta confirmarlo
  antes de enseñar la web al dueño.
- **Carta completa**: la carta consultada en TripAdvisor puede no ser la
  carta completa ni estar actualizada a día de hoy — el aviso "la cocina
  de mercado puede traer cambios puntuales" refleja esto explícitamente.
- Los metadatos usan `https://alvarotaiagu.github.io/o-carballo-taperia-web/`
  como dominio de referencia; si el negocio consigue un dominio propio,
  sustituir esa URL en `index.html` (canonical, `og:url`, `og:image`,
  `twitter:image`, JSON-LD) y en `404.html`.

## Validación hecha

- Servido en local (`python -m http.server`) y revisado con Playwright
  (Chromium) en 1440px y 390px, con `reducedMotion: 'reduce'` y con
  `javaScriptEnabled: false`: 0 errores de consola y 0 requests fallidas en
  los cuatro modos.
- Confirmado con un scroll real de principio a fin (rueda del ratón
  simulada) que cada `data-reveal-group` lleva su contenido (incluidas las
  tarjetas `.carta-stamp`, `.cocina-tile`, `.etapa-stop`) a `opacity: 1` al
  pasar por el viewport — una captura con `scrollIntoView` instantáneo no
  es representativa por sí sola para este patrón de motion.
- Menú de secciones a pantalla completa probado por interacción real
  (clic): abre y cierra correctamente, con cierre por Escape y devolución
  de foco al botón.
- Mapa bajo consentimiento probado por clic real: el iframe de Google se
  crea e inserta correctamente tras el clic, en los tres modos con JS
  activo.
