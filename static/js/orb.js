/* ==========================================================================
   JustTech — Liquid Gooey Orb
   Your code from https://codepen.io/TaminoMartinius/pen/MYJEyer verbatim
   (glassy morphing blob + live preset thumbnails + dat.gui), scoped to the
   Services hero stage (#jt-orb-stage) instead of the full browser window.
   Falls back to an animated SVG gooey orb when WebGL2 is unavailable.
   ========================================================================== */
(function () {
    'use strict';

    var stage = document.getElementById('jt-orb-stage');
    if (!stage) { return; }

    const PRESETS = [
        { name: "Aurora", values: { radius: 0.30, deform: 0.36, frequency: 2.0, morphSpeed: 1.30, rotSpeed: 0.12, specular: 1.0, shininess: 140, glowStrength: 0.70, colorBlue: "#4099FF", colorMagenta: "#E633BF", glowA: "#33B5FF", glowB: "#E24DD0", liquidSpeed: 0.50, liquidScale: 2.20, liquidBright: 1.00, filament: 1.40, core: 0.30, background: "#070A18" } },
        { name: "Ember", values: { radius: 0.32, deform: 0.30, frequency: 2.1, morphSpeed: 1.40, rotSpeed: 0.10, specular: 1.2, shininess: 120, glowStrength: 0.85, colorBlue: "#FFC24D", colorMagenta: "#FF3B2F", glowA: "#FF7A18", glowB: "#FF2D55", liquidSpeed: 0.75, liquidScale: 2.40, liquidBright: 1.10, filament: 1.90, core: 0.40, background: "#160806" } },
        { name: "Toxic", values: { radius: 0.28, deform: 0.44, frequency: 2.3, morphSpeed: 1.50, rotSpeed: 0.18, specular: 1.0, shininess: 160, glowStrength: 0.75, colorBlue: "#9CFF4D", colorMagenta: "#00E5A0", glowA: "#57FF3C", glowB: "#00FFC8", liquidSpeed: 0.85, liquidScale: 2.60, liquidBright: 1.00, filament: 1.70, core: 0.25, background: "#04120C" } },
        { name: "Ice", values: { radius: 0.34, deform: 0.20, frequency: 1.8, morphSpeed: 1.18, rotSpeed: 0.08, specular: 1.5, shininess: 210, glowStrength: 0.60, colorBlue: "#9CE3FF", colorMagenta: "#E6F7FF", glowA: "#6FD2FF", glowB: "#BFEFFF", liquidSpeed: 0.32, liquidScale: 2.00, liquidBright: 0.90, filament: 1.00, core: 0.35, background: "#0A1424" } },
        { name: "Plasma", values: { radius: 0.28, deform: 0.40, frequency: 2.4, morphSpeed: 1.60, rotSpeed: 0.20, specular: 1.0, shininess: 130, glowStrength: 0.95, colorBlue: "#B14DFF", colorMagenta: "#FF2DA0", glowA: "#9B5CFF", glowB: "#FF3DBE", liquidSpeed: 1.00, liquidScale: 2.80, liquidBright: 1.20, filament: 2.10, core: 0.30, background: "#10061C" } },
        { name: "Ghost", values: { radius: 0.32, deform: 0.30, frequency: 2.0, morphSpeed: 1.25, rotSpeed: 0.10, specular: 1.6, shininess: 220, glowStrength: 0.55, colorBlue: "#C2CBE6", colorMagenta: "#8893B5", glowA: "#AEB8D8", glowB: "#6E7799", liquidSpeed: 0.45, liquidScale: 2.20, liquidBright: 0.85, filament: 1.20, core: 0.20, background: "#070709" } },
        { name: "Daylight", values: { radius: 0.30, deform: 0.34, frequency: 2.0, morphSpeed: 1.30, rotSpeed: 0.12, specular: 1.0, shininess: 150, glowStrength: 0.80, colorBlue: "#2D6CFF", colorMagenta: "#B43CF0", glowA: "#3A82FF", glowB: "#A84DFF", liquidSpeed: 0.50, liquidScale: 2.20, liquidBright: 1.05, filament: 1.50, core: 0.30, background: "#EEF2F8" } },
    ];

    function twoDigits(n) {
        return n < 10 ? "0" + n : String(n);
    }

    function updateReadout(i) {
        var nameEl = document.getElementById("jt-orb-current-name");
        if (nameEl) { nameEl.textContent = PRESETS[i].name; }
        var counter = document.getElementById("jt-orb-counter");
        if (counter) {
            counter.textContent = twoDigits(i + 1) + " / " + twoDigits(PRESETS.length);
        }
    }

    function preparePresetContainer() {
        var container = document.getElementById("presets");
        if (!container) { return null; }
        container.removeAttribute("aria-hidden");
        container.setAttribute("aria-label", container.getAttribute("data-label") || "Choose a look");
        return container;
    }

    var canvas = document.getElementById('orb');
    if (!canvas) { gooeyFallback(); return; }

    var gl = null;
    try {
        gl = canvas.getContext('webgl2', { antialias: false, alpha: false });
    } catch (e) { gl = null; }
    if (!gl) {
        if (typeof window.console !== 'undefined' && window.console.warn) {
            window.console.warn('[jt-orb] WebGL2 not supported, using SVG gooey orb');
        }
        gooeyFallback();
        return;
    }

    try {
        orbMain();
    } catch (err) {
        if (typeof window.console !== 'undefined' && window.console.warn) {
            window.console.warn('[jt-orb] boot failed, using SVG gooey orb:', err);
        }
        gooeyFallback();
        return;
    }

    /* =====================================================================
       Fallback — animated SVG gooey blob (no WebGL needed)
       ===================================================================== */
    function gooeyFallback() {
        if (canvas && canvas.parentNode) { canvas.parentNode.removeChild(canvas); }
        stage.classList.add('jt-orb-fallback');
        var activePreset = 0;

        var NS = 'http://www.w3.org/2000/svg';
        var root = document.documentElement;
        var svg = document.createElementNS(NS, 'svg');
        svg.setAttribute('viewBox', '0 0 400 400');

        var defs = document.createElementNS(NS, 'defs');

        var filter = document.createElementNS(NS, 'filter');
        filter.id = 'jt-goo-f';
        var blur = document.createElementNS(NS, 'feGaussianBlur');
        blur.setAttribute('stdDeviation', '14');
        var cm = document.createElementNS(NS, 'feColorMatrix');
        cm.setAttribute('values', '1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 19 -9');
        filter.appendChild(blur);
        filter.appendChild(cm);
        defs.appendChild(filter);

        var soft = document.createElementNS(NS, 'filter');
        soft.id = 'jt-goo-soft';
        var softB = document.createElementNS(NS, 'feGaussianBlur');
        softB.setAttribute('stdDeviation', '7');
        soft.appendChild(softB);
        defs.appendChild(soft);

        var fill = document.createElementNS(NS, 'radialGradient');
        fill.id = 'jt-goo-fill';
        var f1 = document.createElementNS(NS, 'stop');
        f1.setAttribute('offset', '0%');
        f1.setAttribute('stop-color', 'var(--jt-goo-hi)');
        var f2 = document.createElementNS(NS, 'stop');
        f2.setAttribute('offset', '55%');
        f2.setAttribute('stop-color', 'var(--jt-goo-a)');
        var f3 = document.createElementNS(NS, 'stop');
        f3.setAttribute('offset', '100%');
        f3.setAttribute('stop-color', 'var(--jt-goo-dark)');
        fill.appendChild(f1);
        fill.appendChild(f2);
        fill.appendChild(f3);
        defs.appendChild(fill);

        var halo = document.createElementNS(NS, 'radialGradient');
        halo.id = 'jt-goo-halo';
        var h1 = document.createElementNS(NS, 'stop');
        h1.setAttribute('offset', '0%');
        h1.setAttribute('stop-color', 'var(--jt-goo-a)');
        h1.setAttribute('stop-opacity', '0.3');
        var h2 = document.createElementNS(NS, 'stop');
        h2.setAttribute('offset', '100%');
        h2.setAttribute('stop-color', 'var(--jt-goo-a)');
        h2.setAttribute('stop-opacity', '0');
        halo.appendChild(h1);
        halo.appendChild(h2);
        defs.appendChild(halo);

        svg.appendChild(defs);

        var haloRing = document.createElementNS(NS, 'circle');
        haloRing.setAttribute('cx', '200');
        haloRing.setAttribute('cy', '200');
        haloRing.setAttribute('r', '150');
        haloRing.setAttribute('fill', 'url(#jt-goo-halo)');
        svg.appendChild(haloRing);

        var blobG = document.createElementNS(NS, 'g');
        blobG.setAttribute('filter', 'url(#jt-goo-f)');

        var core = document.createElementNS(NS, 'circle');
        core.setAttribute('r', '120');
        core.setAttribute('fill', 'url(#jt-goo-fill)');
        blobG.appendChild(core);

        var NAT = 9;
        var sats = [];
        for (var i = 0; i < NAT; i++) {
            var s = document.createElementNS(NS, 'circle');
            s.setAttribute('fill', 'url(#jt-goo-fill)');
            blobG.appendChild(s);
            sats.push(s);
        }
        svg.appendChild(blobG);

        var liq1 = document.createElementNS(NS, 'circle');
        liq1.setAttribute('fill', 'var(--jt-goo-b)');
        liq1.setAttribute('opacity', '0.7');
        svg.appendChild(liq1);

        var liq2 = document.createElementNS(NS, 'circle');
        liq2.setAttribute('fill', 'var(--jt-goo-hi)');
        liq2.setAttribute('opacity', '0.55');
        liq2.setAttribute('filter', 'url(#jt-goo-soft)');
        svg.appendChild(liq2);

        var hi = document.createElementNS(NS, 'ellipse');
        hi.setAttribute('rx', '64');
        hi.setAttribute('ry', '42');
        hi.setAttribute('fill', '#ffffff');
        hi.setAttribute('opacity', '0.5');
        hi.setAttribute('filter', 'url(#jt-goo-soft)');
        svg.appendChild(hi);

        var orbWindow = document.getElementById('jt-orb-window');
        if (orbWindow) { orbWindow.appendChild(svg); } else { stage.appendChild(svg); }

        function syncTheme() {
            var values = PRESETS[activePreset].values;
            root.style.setProperty('--jt-goo-hi', values.colorMagenta);
            root.style.setProperty('--jt-goo-a', values.colorBlue);
            root.style.setProperty('--jt-goo-dark', values.glowB);
            root.style.setProperty('--jt-goo-b', values.glowA);
        }

        function setupFallbackPresets() {
            var container = preparePresetContainer();
            if (!container) { return; }
            while (container.firstChild) { container.removeChild(container.firstChild); }

            PRESETS.forEach(function (preset, i) {
                var button = document.createElement('button');
                button.type = 'button';
                button.className = i === activePreset ? 'preset is-active' : 'preset';
                button.title = preset.name;
                button.setAttribute('aria-pressed', i === activePreset ? 'true' : 'false');

                var thumb = document.createElement('span');
                thumb.className = 'preset__thumb';
                thumb.style.setProperty('--thumb-hi', preset.values.colorMagenta);
                thumb.style.setProperty('--thumb-a', preset.values.colorBlue);
                thumb.style.setProperty('--thumb-b', preset.values.glowB);

                var name = document.createElement('span');
                name.className = 'preset__name';
                name.textContent = preset.name;

                button.append(thumb, name);
                button.addEventListener('click', function () {
                    activePreset = i;
                    syncTheme();
                    updateReadout(i);
                    Array.prototype.forEach.call(container.querySelectorAll('.preset'), function (el, idx) {
                        el.classList.toggle('is-active', idx === i);
                        el.setAttribute('aria-pressed', idx === i ? 'true' : 'false');
                    });
                });

                container.appendChild(button);
            });

            updateReadout(activePreset);
        }

        setupFallbackPresets();
        syncTheme();
        if (typeof MutationObserver !== 'undefined') {
            new MutationObserver(syncTheme).observe(root, { attributes: true, attributeFilter: ['class'] });
        }

        var start = performance.now();
        function frame(now) {
            var t = (now - start) / 1000;
            var ph = (t % 8) / 8;
            var ease = (function easeInOut(e) { return e < 0.5 ? 4 * e * e * e : 1 - Math.pow(-2 * e + 2, 3) / 2; })(ph);

            var R = 42 + 46 * ease;
            for (var i = 0; i < NAT; i++) {
                var ang = t * 1.15 + (i / NAT) * Math.PI * 2;
                sats[i].setAttribute('cx', 200 + Math.cos(ang) * R);
                sats[i].setAttribute('cy', 200 + Math.sin(ang) * R * 0.88);
                sats[i].setAttribute('r', 36 - 12 * ease + 5 * Math.sin(t * 1.6 + i * 2.1));
            }

            var wob = Math.sin(t * 1.2) * 7 + Math.sin(t * 0.45) * 5;
            core.setAttribute('r', 120 + wob);
            core.setAttribute('cx', 200 + 5 * Math.sin(t * 0.7));
            core.setAttribute('cy', 200 + 4 * Math.cos(t * 0.55));

            liq1.setAttribute('r', 60 + 4 * Math.sin(t * 0.9));
            liq1.setAttribute('cx', 200 + 24 * Math.sin(t * 1.5));
            liq1.setAttribute('cy', 200 + 18 * Math.cos(t * 1.2));
            liq2.setAttribute('r', 36 + 5 * Math.sin(t * 1.1));
            liq2.setAttribute('cx', 200 + 30 * Math.cos(t * 1.3 + 1));
            liq2.setAttribute('cy', 200 + 24 * Math.sin(t * 0.95 + 1));

            hi.setAttribute('cx', 200 + 6 * Math.sin(t * 0.7) - 38);
            hi.setAttribute('cy', 200 + 4 * Math.cos(t * 0.55) - 40);

            requestAnimationFrame(frame);
        }
        requestAnimationFrame(frame);
    }

    /* =====================================================================
       The pen's code (MYJEyer) — scoped to #jt-orb-stage
       ===================================================================== */
    function orbMain() {
        const params = {
            radius: 0.30,
            deform: 0.36,
            frequency: 1.0,
            morphSpeed: 0.30,
            rotSpeed: 0.12,
            specular: 1.0,
            shininess: 140,
            glowStrength: 0.70,
            colorBlue: "#4099FF",
            colorMagenta: "#E633BF",
            glowA: "#33B5FF",
            glowB: "#E24DD0",
            liquidSpeed: 0.50,
            liquidScale: 2.20,
            liquidBright: 1.00,
            filament: 1.40,
            core: 0.30,
            background: "#070A18",
            blend: "Auto",
        };

        // -------------------------------------------------------------------
        // Shaders
        // -------------------------------------------------------------------
        const VERT = `#version 300 es
layout(location=0) in vec2 a_pos;
out vec2 v_uv;
void main(){ v_uv = a_pos * 0.5 + 0.5; gl_Position = vec4(a_pos, 0.0, 1.0); }`;

        const FRAG = `#version 300 es
precision highp float;
in vec2 v_uv;
out vec4 fragColor;

uniform float u_time;
uniform vec2  u_res;
uniform float u_radius;
uniform float u_deform;
uniform float u_freq;
uniform float u_morphSpeed;
uniform float u_rotSpeed;
uniform float u_specular;
uniform float u_shininess;
uniform float u_glowStrength;
uniform vec3  u_colBlue;
uniform vec3  u_colMag;
uniform vec3  u_glowA;
uniform vec3  u_glowB;
uniform float u_liquidSpeed;
uniform float u_liquidScale;
uniform float u_liquidBright;
uniform float u_filament;
uniform float u_core;
uniform vec3  u_bg;
uniform float u_blend;
uniform float u_shift;

mat2 rot(float a){ float c=cos(a), s=sin(a); return mat2(c,-s,s,c); }

float blobField(vec3 p){
  float t = u_time * u_morphSpeed;
  float f = u_freq;
  float d = 0.0;
  d += sin(p.x * 2.6 * f + t * 1.00);
  d += sin(p.y * 2.9 * f - t * 0.80 + 1.3);
  d += sin(p.z * 3.2 * f + t * 1.20 + 2.7);
  d += sin((p.x + p.z) * 2.2 * f - t * 0.90 + 4.1);
  d += sin((p.y - p.x) * 2.4 * f + t * 0.70 + 0.6);
  return d * 0.2;
}

float mapBlob(vec3 p){
  float t = u_time * u_rotSpeed;
  p.xy *= rot(t * 0.7);
  p.yz *= rot(t * 0.5);
  float r = u_radius + u_deform * blobField(p);
  return length(p) - r;
}

vec3 calcNormal(vec3 p){
  vec2 e = vec2(0.0015, 0.0);
  return normalize(vec3(
    mapBlob(p + e.xyy) - mapBlob(p - e.xyy),
    mapBlob(p + e.yxy) - mapBlob(p - e.yxy),
    mapBlob(p + e.yyx) - mapBlob(p - e.yyx)));
}

float hash13(vec3 p3){ p3 = fract(p3 * 0.1031); p3 += dot(p3, p3.zyx + 31.32); return fract((p3.x + p3.y) * p3.z); }
float vnoise3(vec3 p){
  vec3 i = floor(p), f = fract(p); f = f * f * (3.0 - 2.0 * f);
  return mix(mix(mix(hash13(i + vec3(0,0,0)), hash13(i + vec3(1,0,0)), f.x),
                 mix(hash13(i + vec3(0,1,0)), hash13(i + vec3(1,1,0)), f.x), f.y),
             mix(mix(hash13(i + vec3(0,0,1)), hash13(i + vec3(1,0,1)), f.x),
                 mix(hash13(i + vec3(0,1,1)), hash13(i + vec3(1,1,1)), f.x), f.y), f.z);
}
float fbm3(vec3 p){ float v = 0.0, a = 0.5; for (int i = 0; i < 3; i++){ v += a * vnoise3(p); p *= 2.03; a *= 0.5; } return v; }

float liquid(vec3 p){
  float t = u_time * u_liquidSpeed;
  p *= u_liquidScale;
  p.xy *= rot(t * 0.15);
  p.yz *= rot(t * 0.10);
  vec3 w = vec3(fbm3(p + t * 0.2), fbm3(p + vec3(4.3, 1.2, -t * 0.15)), fbm3(p.zxy + vec3(7.7, 2.3, t * 0.10)));
  return fbm3(p + 1.8 * w);
}

void main(){
  vec2 p = v_uv * 2.0 - 1.0;
  p.x *= u_res.x / u_res.y;
  p.x -= u_shift;

  vec3 ro = vec3(0.0, 0.0, 3.0);
  vec3 rd = normalize(vec3(p, -1.8));

  float t = 0.0;
  bool hit = false;
  vec3 pos = ro;
  float minD = 1e3;
  for (int i = 0; i < 160; i++) {
    pos = ro + rd * t;
    float d = mapBlob(pos);
    minD = min(minD, d);
    if (d < 0.001) { hit = true; break; }
    t += d * 0.40;
    if (t > 6.0) break;
  }

  vec3 E = vec3(0.0);

  if (hit) {
    vec3 n = calcNormal(pos);
    vec3 v = -rd;
    float fres = pow(1.0 - max(dot(n, v), 0.0), 3.0);

    vec3 rp = pos + rd * 0.04;
    float trans = 1.0;
    vec3 inner = vec3(0.0);
    for (int k = 0; k < 10; k++) {
      float raw = liquid(rp);
      float dens = smoothstep(0.30, 0.70, raw);
      float fil = pow(1.0 - abs(2.0 * raw - 1.0), 5.0);
      vec3 c = mix(u_colMag, u_colBlue, 0.5 + 0.5 * sin(raw * 6.0 + u_time * 0.3 + rp.y * 2.5));
      vec3 emit = c * dens * 0.55 + c * fil * u_filament + vec3(1.0) * pow(fil, 3.0) * u_filament * 0.4;
      emit += u_colBlue * smoothstep(0.5, 0.0, length(rp)) * u_core;
      inner += trans * emit * 0.17;
      trans *= 0.84;
      rp += rd * 0.11;
      if (length(rp) > 1.0) break;
    }
    E += inner * (1.0 - fres * 0.6) * u_liquidBright;

    vec3 rim = mix(u_colMag, u_colBlue, 0.5 + 0.5 * (n.x * 0.7 + n.y * 0.45));
    E += rim * fres * 1.3;
    vec3 l1 = normalize(vec3(0.6, 0.85, 0.6));
    vec3 l2 = normalize(vec3(-0.7, 0.25, 0.55));
    vec3 h1 = normalize(l1 + v);
    vec3 h2 = normalize(l2 + v);
    E += vec3(1.0) * pow(max(dot(n, h1), 0.0), u_shininess) * 1.3 * u_specular;
    E += vec3(0.8, 0.9, 1.0) * pow(max(dot(n, h2), 0.0), u_shininess * 0.45) * 0.6 * u_specular;
  } else {
    float g = exp(-minD * 5.5);
    float ang = atan(rd.y, rd.x);
    vec3 gc = mix(u_glowA, u_glowB, 0.5 + 0.5 * sin(ang * 3.0 + u_time * 0.5));
    E += (gc * g * 1.4 + vec3(0.6, 0.8, 1.0) * pow(g, 3.0) * 0.7) * u_glowStrength;
  }

  vec3 glowCol = u_bg + E;
  float cov = clamp(max(E.r, max(E.g, E.b)), 0.0, 1.0);
  vec3 inkCol = mix(u_bg, E / (1.0 + E), cov);
  vec3 col = mix(glowCol, inkCol, u_blend);

  fragColor = vec4(clamp(col, 0.0, 1.0), 1.0);
}`;

        // -------------------------------------------------------------------
        // WebGL plumbing
        // -------------------------------------------------------------------
        function compile(type, src) {
            const sh = gl.createShader(type);
            gl.shaderSource(sh, src);
            gl.compileShader(sh);
            if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
                throw new Error(gl.getShaderInfoLog(sh) || "shader compile failed");
            }
            return sh;
        }
        const program = gl.createProgram();
        gl.attachShader(program, compile(gl.VERTEX_SHADER, VERT));
        gl.attachShader(program, compile(gl.FRAGMENT_SHADER, FRAG));
        gl.linkProgram(program);
        if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
            throw new Error(gl.getProgramInfoLog(program) || "link failed");
        }
        gl.useProgram(program);

        const vao = gl.createVertexArray();
        gl.bindVertexArray(vao);
        const buf = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, buf);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
        gl.enableVertexAttribArray(0);
        gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);

        const U = {
            time: gl.getUniformLocation(program, "u_time"),
            res: gl.getUniformLocation(program, "u_res"),
            radius: gl.getUniformLocation(program, "u_radius"),
            deform: gl.getUniformLocation(program, "u_deform"),
            freq: gl.getUniformLocation(program, "u_freq"),
            morphSpeed: gl.getUniformLocation(program, "u_morphSpeed"),
            rotSpeed: gl.getUniformLocation(program, "u_rotSpeed"),
            specular: gl.getUniformLocation(program, "u_specular"),
            shininess: gl.getUniformLocation(program, "u_shininess"),
            glowStrength: gl.getUniformLocation(program, "u_glowStrength"),
            colBlue: gl.getUniformLocation(program, "u_colBlue"),
            colMag: gl.getUniformLocation(program, "u_colMag"),
            glowA: gl.getUniformLocation(program, "u_glowA"),
            glowB: gl.getUniformLocation(program, "u_glowB"),
            liquidSpeed: gl.getUniformLocation(program, "u_liquidSpeed"),
            liquidScale: gl.getUniformLocation(program, "u_liquidScale"),
            liquidBright: gl.getUniformLocation(program, "u_liquidBright"),
            filament: gl.getUniformLocation(program, "u_filament"),
            core: gl.getUniformLocation(program, "u_core"),
            bg: gl.getUniformLocation(program, "u_bg"),
            blend: gl.getUniformLocation(program, "u_blend"),
            shift: gl.getUniformLocation(program, "u_shift"),
        };

        function hexToRgb(hex) {
            let h = hex.replace("#", "");
            if (h.length === 3) { h = h.split("").map((c) => c + c).join(""); }
            const n = parseInt(h, 16);
            return [((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255];
        }
        function luminance(hex) {
            const [r, g, b] = hexToRgb(hex);
            return 0.299 * r + 0.587 * g + 0.114 * b;
        }
        function pageBg() {
            return "#000000";
        }
        function blendFor(v, bgHex) {
            if (params.blend === "Glow") { return 0; }
            if (params.blend === "Ink") { return 1; }
            return Math.min(Math.max((luminance(bgHex) - 0.35) / 0.30, 0), 1);
        }

        // keep the stage background in sync with the orb (always black)
        function syncChrome() {
            const bg = "#000000";
            stage.style.background = bg;
            stage.style.setProperty("--page-bg", bg);
        }

        function drawOrb(x, y, w, h, v, time, shift, bgHex) {
            const b = bgHex || v.background;
            gl.viewport(x, y, w, h);
            gl.scissor(x, y, w, h);
            const bc = hexToRgb(b);
            gl.clearColor(bc[0], bc[1], bc[2], 1.0);
            gl.clear(gl.COLOR_BUFFER_BIT);
            gl.uniform1f(U.time, time);
            gl.uniform2f(U.res, w, h);
            gl.uniform1f(U.shift, shift || 0);
            gl.uniform1f(U.radius, v.radius);
            gl.uniform1f(U.deform, v.deform);
            gl.uniform1f(U.freq, v.frequency);
            gl.uniform1f(U.morphSpeed, v.morphSpeed);
            gl.uniform1f(U.rotSpeed, v.rotSpeed);
            gl.uniform1f(U.specular, v.specular);
            gl.uniform1f(U.shininess, v.shininess);
            gl.uniform1f(U.glowStrength, v.glowStrength);
            gl.uniform3fv(U.colBlue, hexToRgb(v.colorBlue));
            gl.uniform3fv(U.colMag, hexToRgb(v.colorMagenta));
            gl.uniform3fv(U.glowA, hexToRgb(v.glowA));
            gl.uniform3fv(U.glowB, hexToRgb(v.glowB));
            gl.uniform1f(U.liquidSpeed, v.liquidSpeed);
            gl.uniform1f(U.liquidScale, v.liquidScale);
            gl.uniform1f(U.liquidBright, v.liquidBright);
            gl.uniform1f(U.filament, v.filament);
            gl.uniform1f(U.core, v.core);
            gl.uniform3fv(U.bg, hexToRgb(b));
            gl.uniform1f(U.blend, blendFor(v, b));
            gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
        }

        const presetsContainer = preparePresetContainer();
        const presetEls = [];
        const previews = [];

        function applyPreset(i) {
            Object.assign(params, PRESETS[i].values);
            syncChrome();
            updateReadout(i);
            presetEls.forEach((el, idx) => {
                const active = idx === i;
                el.classList.toggle("is-active", active);
                el.setAttribute("aria-pressed", active ? "true" : "false");
            });
        }

        if (presetsContainer) {
            PRESETS.forEach((preset, i) => {
                const wrap = document.createElement("button");
                wrap.type = "button";
                wrap.className = "preset";
                wrap.title = preset.name;
                wrap.setAttribute("aria-pressed", "false");
                const thumb = document.createElement("span");
                thumb.className = "preset__thumb";
                const name = document.createElement("span");
                name.className = "preset__name";
                name.textContent = preset.name;
                wrap.append(thumb, name);
                wrap.addEventListener("click", () => applyPreset(i));
                presetsContainer.append(wrap);
                presetEls.push(wrap);
                previews.push({ el: thumb, values: preset.values });
            });
        }
        applyPreset(0);

        let dpr = 1;

        function resize() {
            dpr = Math.min(window.devicePixelRatio || 1, 1.5);
            const w = Math.max(1, Math.floor(stage.clientWidth * dpr));
            const h = Math.max(1, Math.floor(stage.clientHeight * dpr));
            if (canvas.width !== w || canvas.height !== h) {
                canvas.width = w;
                canvas.height = h;
            }
        }
        window.addEventListener("resize", resize);
        resize();

        function canvasRect(el, stageRect) {
            const r = el.getBoundingClientRect();
            return {
                x: Math.floor((r.left - stageRect.left) * dpr),
                y: Math.floor((stageRect.bottom - r.bottom) * dpr),
                w: Math.ceil(r.width * dpr),
                h: Math.ceil(r.height * dpr),
                bottom: r.bottom,
                top: r.top,
            };
        }

        const orbWindow = document.getElementById("jt-orb-window") || stage;

        function frame(now) {
            resize();
            const time = now * 0.001;
            const themeHex = pageBg();
            const themeRgb = hexToRgb(themeHex);
            gl.clearColor(themeRgb[0], themeRgb[1], themeRgb[2], 1.0);
            gl.disable(gl.SCISSOR_TEST);
            gl.clear(gl.COLOR_BUFFER_BIT);
            gl.enable(gl.SCISSOR_TEST);

            const stageRect = stage.getBoundingClientRect();
            const mainRect = canvasRect(orbWindow, stageRect);
            if (mainRect.w > 0 && mainRect.h > 0) {
                drawOrb(mainRect.x, mainRect.y, mainRect.w, mainRect.h, params, time, 0, themeHex);
            }

            for (const pv of previews) {
                const r = canvasRect(pv.el, stageRect);
                if (r.w <= 0 || r.h <= 0 || r.bottom <= stageRect.top || r.top >= stageRect.bottom) { continue; }
                drawOrb(r.x, r.y, r.w, r.h, pv.values, time, 0);
            }
            requestAnimationFrame(frame);
        }

        if (typeof MutationObserver !== "undefined") {
            new MutationObserver(function () { syncChrome(); })
                .observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });
        }
        requestAnimationFrame(frame);
    }
})();