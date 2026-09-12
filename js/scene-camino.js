/* ---------- Hero: sendero de señalización con veneras y flechas ----------
   Gráfico de ruta, no una escena ilustrada: una línea de camino discontinua
   que fluye de izquierda a derecha (como un plano de sendero) con tres
   marcas de señalización reales del Camino de Santiago — la venera y la
   flecha direccional, símbolos públicos de wayfinding, no clip-art
   genérico — pulsando suavemente en sus paradas. Ninguna web hermana usa
   esta técnica: Melao usa un shader de blobs, A Taberna do Rio y
   O Logradouro usan iconos de platos orbitando (con y sin acabado gooey),
   Marabú usa partículas ambiente. Canvas 2D, DPR limitado a 2, pausado
   fuera de viewport/pestaña oculta, con render estático bajo
   prefers-reduced-motion. El <canvas> es aria-hidden y se dibuja sobre el
   degradado azul del propio .hero, que sigue siendo un fondo completo si
   el canvas no se inicializa. */
(function () {
  function drawShellMark(ctx, x, y, r, fillColor, strokeColor) {
    ctx.save();
    ctx.translate(x, y);
    ctx.beginPath();
    ctx.arc(0, r * 0.15, r, Math.PI * 1.12, Math.PI * 1.88);
    ctx.closePath();
    ctx.fillStyle = fillColor;
    ctx.fill();
    ctx.strokeStyle = strokeColor;
    ctx.lineWidth = Math.max(1, r * 0.09);
    ctx.stroke();
    const rays = 6;
    for (let i = 0; i <= rays; i++) {
      const a = Math.PI * 1.12 + ((Math.PI * 1.88 - Math.PI * 1.12) * i) / rays;
      ctx.beginPath();
      ctx.moveTo(0, r * 0.15);
      ctx.lineTo(Math.cos(a) * r, r * 0.15 + Math.sin(a) * r);
      ctx.stroke();
    }
    ctx.restore();
  }

  function drawArrowMark(ctx, x, y, size, angle, color) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(angle);
    ctx.beginPath();
    ctx.moveTo(-size * 0.55, -size * 0.4);
    ctx.lineTo(size * 0.55, 0);
    ctx.lineTo(-size * 0.55, size * 0.4);
    ctx.lineTo(-size * 0.22, 0);
    ctx.closePath();
    ctx.fillStyle = color;
    ctx.fill();
    ctx.restore();
  }

  // Puntos de control del sendero, en fracciones de (width, height) — un
  // trazado suave que sube de izquierda a derecha, con espacio a la
  // izquierda para el titular del hero.
  const ROUTE = [
    { x: 0.42, y: 0.82 },
    { x: 0.55, y: 0.7 },
    { x: 0.62, y: 0.78 },
    { x: 0.72, y: 0.55 },
    { x: 0.84, y: 0.42 },
    { x: 0.98, y: 0.3 },
  ];
  const MARKERS = [
    { t: 0.18, type: "shell" },
    { t: 0.5, type: "arrow" },
    { t: 0.82, type: "shell" },
  ];

  function pointAt(t, w, h) {
    const segCount = ROUTE.length - 1;
    const segF = Math.min(t, 0.9999) * segCount;
    const seg = Math.floor(segF);
    const localT = segF - seg;
    const a = ROUTE[seg];
    const b = ROUTE[Math.min(seg + 1, ROUTE.length - 1)];
    return {
      x: (a.x + (b.x - a.x) * localT) * w,
      y: (a.y + (b.y - a.y) * localT) * h,
      angle: Math.atan2((b.y - a.y) * h, (b.x - a.x) * w),
    };
  }

  window.createCaminoScene = function createCaminoScene(canvas) {
    const ctx = canvas.getContext("2d");
    if (!ctx) return null;

    let dpr = Math.min(window.devicePixelRatio || 1, 2);
    let width = 0,
      height = 0;
    let pointer = { x: 0, y: 0 };
    let t = 0;
    let raf = null;
    let running = false;

    function resize() {
      const rect = canvas.getBoundingClientRect();
      width = rect.width;
      height = rect.height;
      canvas.width = Math.max(1, Math.round(width * dpr));
      canvas.height = Math.max(1, Math.round(height * dpr));
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    function onPointerMove(e) {
      const rect = canvas.getBoundingClientRect();
      pointer.x = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
      pointer.y = ((e.clientY - rect.top) / rect.height - 0.5) * 2;
    }
    function onPointerLeave() {
      pointer.x = 0;
      pointer.y = 0;
    }

    function frame() {
      ctx.clearRect(0, 0, width, height);
      const leanX = pointer.x * 10;
      const leanY = pointer.y * 8;

      ctx.save();
      ctx.translate(leanX, leanY);

      // Trazado del sendero
      ctx.beginPath();
      ROUTE.forEach((p, i) => {
        const x = p.x * width;
        const y = p.y * height;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      });
      ctx.strokeStyle = "rgba(246, 240, 228, 0.32)";
      ctx.lineWidth = Math.max(2, width * 0.0028);
      ctx.setLineDash([width * 0.018, width * 0.014]);
      ctx.lineDashOffset = -t * 60;
      ctx.lineCap = "round";
      ctx.lineJoin = "round";
      ctx.stroke();
      ctx.setLineDash([]);

      // Marcas de señalización en paradas fijas del sendero
      MARKERS.forEach((m, i) => {
        const p = pointAt(m.t, width, height);
        const pulse = 1 + Math.sin(t * 1.6 + i * 2.1) * 0.08;
        const r = Math.min(width, height) * 0.026 * pulse;
        if (m.type === "shell") {
          drawShellMark(ctx, p.x, p.y, r, "#D9A21B", "#14293C");
        } else {
          drawArrowMark(ctx, p.x, p.y, r * 2.1, p.angle, "#D9A21B");
        }
      });

      // Punto de luz recorriendo el sendero en bucle, sugiriendo el sentido
      // de la marcha hacia Santiago.
      const travel = (t * 0.09) % 1;
      const lp = pointAt(travel, width, height);
      const grad = ctx.createRadialGradient(lp.x, lp.y, 0, lp.x, lp.y, Math.min(width, height) * 0.05);
      grad.addColorStop(0, "rgba(246, 240, 228, 0.9)");
      grad.addColorStop(1, "rgba(246, 240, 228, 0)");
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.arc(lp.x, lp.y, Math.min(width, height) * 0.05, 0, Math.PI * 2);
      ctx.fill();

      ctx.restore();
    }

    function loop() {
      if (!running) return;
      t += 0.016;
      frame();
      raf = requestAnimationFrame(loop);
    }

    function start() {
      if (running) return;
      running = true;
      raf = requestAnimationFrame(loop);
    }
    function stop() {
      running = false;
      if (raf) cancelAnimationFrame(raf);
      raf = null;
    }

    resize();
    frame();

    const onResize = () => {
      resize();
      frame();
    };
    window.addEventListener("resize", onResize);
    canvas.addEventListener("pointermove", onPointerMove);
    canvas.addEventListener("pointerleave", onPointerLeave);

    let io = null;
    if ("IntersectionObserver" in window) {
      io = new IntersectionObserver(
        ([entry]) => {
          if (entry.isIntersecting && !document.hidden) start();
          else stop();
        },
        { threshold: 0.05 }
      );
      io.observe(canvas);
    } else {
      start();
    }

    function onVisibility() {
      if (document.hidden) stop();
      else {
        const rect = canvas.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom > 0) start();
      }
    }
    document.addEventListener("visibilitychange", onVisibility);

    return {
      destroy() {
        stop();
        window.removeEventListener("resize", onResize);
        canvas.removeEventListener("pointermove", onPointerMove);
        canvas.removeEventListener("pointerleave", onPointerLeave);
        document.removeEventListener("visibilitychange", onVisibility);
        if (io) io.disconnect();
      },
    };
  };
})();
