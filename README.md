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

## Actualización con assets reales (12-09-2026)

La primera versión de este sitio se construyó sin logo ni carta propios
(bloqueo de scraping en Instagram/Facebook), así que usaba un emblema y una
paleta inventados y una carta parcial sacada de TripAdvisor. El mismo día,
el cliente aportó:
- **El logo real**: una hoja de roble en blanco sobre fondo negro con el
  logotipo "O CARBALLO TAPERÍA" (`assets/img/source/logo-original.jpg`).
  Se procesó con `scripts/process_logo.py` (extracción de alfa por
  luminancia, sin recortar a mano) para obtener una marca en blanco sobre
  transparente (`mark-white.png`, fondos oscuros) y en tinta sobre
  transparente (`mark-ink.png`, fondos claros), además de regenerar
  favicons/manifest y la imagen Open Graph con la marca real.
- **La carta real completa**: 7 fotografías de las páginas de la carta
  (`assets/img/source/carta-*.webp`), con 24 platos y precios reales en 7
  apartados (Ensaladas, De la tierra, Vegetales, Del mar, Tostas, Arroces,
  Postres) — sustituye a los 7 platos parciales que se habían sacado del
  OCR de TripAdvisor en la versión anterior. Un dato quedó corregido: "Croca
  de Vaca Fileteada" es el nombre real del plato (ternera gallega
  fileteada) — la v1 lo había "corregido" por error a "Chuleta de vaca
  fileteada" al no tener la carta real todavía.
- La paleta se recalculó a partir de estos assets reales (ver "Dirección de
  arte" abajo) en vez de la paleta azul+amarillo de señalización del Camino
  que se había inventado a falta de logo.

## Corrección: reseñas reales de Google + teléfono (12-09-2026)

Una versión intermedia de este sitio mostró un sello "Travellers' Choice"
de TripAdvisor que un fetch automático había reportado — el usuario lo
señaló como sospechoso (esa distinción es incompatible con las 0 reseñas
que la propia ficha de TripAdvisor mostraba) y se retiró por completo
(ver [[feedback-verify-fetched-achievement-claims]] en la memoria del
workspace). El usuario preguntó entonces si existían reseñas reales en
otro sitio y aportó una captura de pantalla de la **ficha real de Google
Maps del negocio**, que sí existe y tiene reseñas reales:
- **4,9★ sobre 5, 637 reseñas en Google** — mostrado ahora en el hero y en
  `#reconocimientos` (anillo de valoración, mismo componente de datos que
  A Taberna do Rio/O Logradouro, con la cifra real esta vez).
- **Servicios reales confirmados por la ficha de Google**: terraza,
  opciones vegetarianas, música en directo — añadidos como chips en la
  misma sección y al `amenityFeature` del JSON-LD.
- **Teléfono**: la ficha de Google muestra **881 30 22 43**, que coincide
  con el de TripAdvisor — no con el 690 02 02 86 que turismo.gal tenía
  registrado. Como 690 02 02 86 sí tiene formato de móvil español (y 881
  no), se mantiene 690 02 02 86 solo para los enlaces de WhatsApp, y se
  cambió 881 30 22 43 a "teléfono principal" (enlaces `tel:`, JSON-LD
  `telephone`) por ser el que coincide entre las dos fichas más
  consultadas (Google y TripAdvisor).
- Precio medio real de la ficha de Google: 20–30 € (añadido a
  `priceRange` en el JSON-LD).

**Por qué esto importa:** ilustra por qué "sin datos verificables, no
mostrar nada" (la postura tomada tras retirar el sello de TripAdvisor) es
mejor que inventar, pero también que vale la pena preguntar antes de
asumir que un dato no existe en ningún sitio — en este caso sí existía,
solo que en otra plataforma (Google, no TripAdvisor).

Además, el usuario autorizó explícitamente usar fotografía de banco libre
(Unsplash License, uso comercial permitido) allí donde aporte valor,
siempre que sea acorde al tipo de cocina — el negocio no facilitó fotos
propias del local ni de los platos servidos. Se añadieron 5 fotografías de
ambiente (bosque de robles, tapas, arroz, marisco, tostas) con el patrón de
carga *blur-up* (LQIP) ya usado en `webtest`, cada una con su crédito visible
y su procedencia documentada en `scripts/process_photos.py`. Ver "Fotografía"
más abajo para el detalle de cada crédito.

## Quinta familia estructural del workspace

Este workspace usa cada web como plantilla reutilizable para vender a
futuros clientes, así que cada sitio debe leerse como una plantilla
distinta, no como un reskin. Antes de escribir una sola línea se revisó la
estructura de las cuatro webs hermanas (Melao, Marabú, A Taberna do Rio,
O Logradouro) para no repetir ni el orden de secciones ni la técnica de
hero de ninguna. El hilo conductor elegido aquí es real y verificable: el
negocio está confirmado en el trazado del **Camino Inglés** (turismo.gal),
en su última etapa antes de Santiago — así que toda la identidad se apoya
en esa geografía real:

- **Hero: sendero de señalización** (`js/scene-camino.js`): un camino
  discontinuo que fluye por el canvas con veneras y flechas — símbolos
  públicos y reales de señalización del Camino de Santiago — pulsando en
  sus paradas y un punto de luz que recorre la ruta. Ninguna web hermana
  usa esta técnica: Melao usa un shader de blobs, A Taberna do Rio y O
  Logradouro usan iconos de platos orbitando (con y sin acabado "gooey"),
  Marabú usa partículas ambiente.
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
  ahora con la **carta real completa** (7 apartados, 24 platos, precios
  reales), a diferencia del foco+índice sin precios de O Logradouro.
  Deliberadamente distinto también de la hoja de precios de A Taberna do
  Rio y del grid de fotos de Melao.
- **"Reseñas"** (`#reconocimientos`): anillo de valoración con la cifra
  REAL de Google (4,9★ / 637 reseñas) — mismo componente de datos que A
  Taberna do Rio/O Logradouro, verificado esta vez con una captura de
  pantalla de la ficha de Google Maps del propio negocio aportada por el
  usuario. Pasó por dos estados antes de esto: primero mostraba un sello
  "Travellers' Choice" de TripAdvisor mal atribuido (ver la sección
  "Corrección: reseñas reales de Google + teléfono" más abajo), luego —
  al no poder verificarlo y no saber todavía de la ficha de Google — una
  invitación honesta a "sé el primero en opinar" sin ninguna cifra. La
  cifra real de Google reemplaza a ambas versiones.

Validado con Playwright (Chromium local) en desktop/mobile, con
`reducedMotion: 'reduce'`, con `javaScriptEnabled: false` y con scroll real
completo (rueda del ratón simulada, no solo `scrollIntoView`, ya que una
captura estática con salto instantáneo no dispara los `ScrollTrigger`):
0 errores de consola y 0 requests fallidas en los cuatro modos.

## Dirección de arte

- **Idea visual:** una tapería en Sigüeiro (Oroso) que es, literalmente, la
  última parada antes de que el Camino Inglés entre en Santiago — de ahí el
  titular "El descanso justo antes de Santiago."
- **Paleta (actualizada 12-09-2026, sacada de assets reales):** el logo
  real es blanco y negro (hoja de roble sobre negro) y la carta real usa
  papel crema con ilustraciones de hoja/bellota en dorado y marrón. La
  paleta se recalculó a partir de eso — `--tinta`/`--marco*` sacan su negro
  del logo real, `--papel`/`--piedra*` su crema de la carta real, y
  `--sendero*`/`--roble*` el dorado y el marrón de la ilustración de la
  carta. `--fraga*` es un verde-oliva de apoyo derivado de la misma familia
  cálida. Los nombres de variable se mantuvieron iguales a la v1 (que se
  apoyaba en el azul y el amarillo de la señalización del Camino, al no
  haber logo todavía) para no reescribir el CSS — solo cambiaron los
  valores. Deliberadamente distinta de: coral/cielo/lima (Melao), verde
  río/madera/dorado (A Taberna do Rio), piedra/barro/vino/oliva (O
  Logradouro). Ver `css/style.css`, bloque `:root`.
- **Tipografía:** Spectral (serif con itálica expresiva) + Manrope (texto e
  interfaz) — pareja propia, distinta de Fraunces+Work Sans (O Logradouro)
  y Bitter+Inter (Melao/A Taberna do Rio).
- **Logo:** el real, aportado por el cliente (`assets/img/source/logo-original.jpg`)
  — una hoja de roble sobre el logotipo "O CARBALLO TAPERÍA". Procesado con
  `scripts/process_logo.py` en dos variantes de fondo transparente
  (`mark-white.png`, `mark-ink.png`) más favicons/manifest/OG regenerados a
  partir de la marca real, no de un emblema inventado.
- **Fotografía — IMPORTANTE:** el negocio no facilitó fotos propias del
  local ni de los platos servidos (solo el logo y las fotos de la carta en
  papel). El usuario autorizó explícitamente usar fotografía de banco libre
  acorde al tipo de cocina para las secciones donde aporte valor. Se
  usaron 5 fotos con licencia Unsplash (uso comercial libre, sin necesidad
  de permiso), cada una marcada como "Fotografía de ambiente" con su
  crédito visible en la propia imagen — **ninguna se presenta como una foto
  real del local o de sus platos servidos**:
  - `#etapa`: bosque de robles en otoño — **David Gabrić**, Unsplash.
  - `#cocina`: tapas caseras — **Nacho Carretero Molero**, Unsplash.
  - `#carta` (Del mar): gambas a la plancha — Unsplash (crédito genérico,
    ficha sin nombre de autor legible en la búsqueda).
  - `#carta` (Tostas): tostas variadas — **Nacho Carretero Molero**, Unsplash.
  - `#carta` (Arroces): arroz meloso de marisco — **Armando Brenlha**, Unsplash.
  Patrón *blur-up* (LQIP) real en archivo (no base64 a mano) igual que en
  `webtest` — ver `scripts/process_photos.py` para la procedencia exacta de
  cada URL y `js/main.js` (`initLqipReveal`) para el mecanismo de carga.
  **Antes de enseñar la web al dueño, lo ideal es sustituir estas fotos de
  banco por fotos reales del local y los platos servidos** en cuanto estén
  disponibles — la estructura del sitio no depende de ellas.
- **Motion:** GSAP + ScrollTrigger para las revelaciones por sección, Lenis
  como motor de scroll suave. Todo el motion es opcional: si el CDN de
  GSAP/Lenis falla, el sitio se degrada con limpieza — menú, horario en
  vivo, mapa y WhatsApp siguen funcionando sin errores de consola.
- **Icons:** Iconify — Solar para símbolos de interfaz, MDI para
  Instagram/Facebook/pescado/pan/arroz/repostería, `ri` para el glifo de
  WhatsApp y `simple-icons:tripadvisor` para el sello real de TripAdvisor.
- **Skill de diseño usada:** `build-awwwards-quality-sites`, con dirección
  de arte propia (paleta, tipografía, contenido y estructura) para este
  negocio.

## Contenido real vs. pendiente

**Confirmado y usado tal cual:**
- Nombre, dirección (Avenida da Grabanxa, 29, Sigüeiro, 15888 Oroso, A
  Coruña), confirmado en el trazado del Camino Inglés (turismo.gal).
- Teléfono principal (881 30 22 43, ficha de Google Maps y de TripAdvisor),
  WhatsApp (690 02 02 86, ficha oficial de turismo.gal) y email
  (manuelfrala@gmail.com, ficha oficial de turismo.gal) — ver "Corrección:
  reseñas reales de Google + teléfono" arriba.
- **Valoración real de Google: 4,9★ / 637 reseñas**, terraza, opciones
  vegetarianas y música en directo confirmados por una captura de pantalla
  de la ficha de Google Maps del negocio aportada directamente por el
  cliente el 12-09-2026.
- Horario: miércoles y jueves 9:00–23:00, viernes 9:00–1:00, sábado
  10:00–1:00, domingo 10:00–23:00, lunes y martes cerrado; cocina
  13:00–16:00 y 21:00–23:30.
- **Logo real** y **carta real completa** (7 apartados, 24 platos, precios
  reales) aportados directamente por el cliente el 12-09-2026 — ver arriba.
- Distancia real Sigüeiro→Santiago (última etapa del Camino Inglés, ~16
  km, cruzando el Ponte do Tambre y la Fraga Encantada) — fuentes públicas
  de operadores del Camino Inglés. Las distancias intermedias de Ponte do
  Tambre y Fraga Encantada en la franja `#etapa` (≈11 km y ≈5 km) son una
  interpolación aproximada sobre el total real de 16 km, no una medición
  propia verificada punto a punto.
- Cuenta de Instagram `@ocarballotaperia` y página de Facebook
  "O Carballo Taperia" (URLs facilitadas directamente por el cliente).

**⚠️ Pendiente / decisiones tomadas por mi cuenta — revisar antes de
enseñar la web:**
- **Fotos reales del local y los platos servidos** (ver "Fotografía"
  arriba) — las 5 fotos de banco deberían sustituirse en cuanto el negocio
  tenga fotografía propia.
- **TripAdvisor sigue sin reseñas propias** (0 en el momento de la
  consulta) y su sello "Travellers' Choice" reportado por un fetch
  automático resultó ser un error — ver
  [[feedback-verify-fetched-achievement-claims]]. La web ya no menciona
  TripAdvisor como fuente de valoración; solo Google (4,9★/637, real).
- **WhatsApp**: se asume que 690 02 02 86 (móvil español) tiene WhatsApp
  activo — falta confirmarlo antes de enseñar la web al dueño. El teléfono
  881 30 22 43 (fijo/VoIP, sin formato de móvil) se usa solo como llamada,
  nunca como enlace de WhatsApp.
- Los metadatos usan `https://alvarotaiagu.github.io/o-carballo-taperia-web/`
  como dominio de referencia; si el negocio consigue un dominio propio,
  sustituir esa URL en `index.html` (canonical, `og:url`, `og:image`,
  `twitter:image`, JSON-LD) y en `404.html`.

## Validación hecha

- Servido en local (`python -m http.server`) y revisado con Playwright
  (Chromium) en 1440px y 390px, con `reducedMotion: 'reduce'` y con
  `javaScriptEnabled: false`: 0 errores de consola y 0 requests fallidas en
  los cuatro modos (comprobado en la v1; pendiente de repetir tras la
  actualización de assets reales — ver historial de la sesión).
- Confirmado con un scroll real de principio a fin (rueda del ratón
  simulada) que cada `data-reveal-group` lleva su contenido (incluidas las
  tarjetas `.carta-stamp`, `.cocina-tile`, `.etapa-stop`, `.photo-frame`) a
  `opacity: 1` al pasar por el viewport.
- Menú de secciones a pantalla completa y mapa bajo consentimiento
  probados por interacción real (clic).
