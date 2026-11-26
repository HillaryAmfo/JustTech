/* ============================================================
   JustTech — main.js
   ============================================================ */

(function () {
    'use strict';

    /* --------------------------------------------------------
       MOBILE MENU
       -------------------------------------------------------- */
    const mobileMenuButton = document.getElementById('mobileMenuButton');
    const mobileMenu = document.getElementById('mobileMenu');
    const closeMobileMenu = document.getElementById('closeMobileMenu');
    const mobileBackdrop = document.getElementById('mobileBackdrop');

    let previousFocus = null;

    function openMobileMenu() {
        if (!mobileMenu) return;
        previousFocus = document.activeElement;

        mobileMenu.classList.add('active');
        if (mobileBackdrop) mobileBackdrop.classList.add('active');
        document.body.classList.add('menu-open');
        if (mobileMenuButton) mobileMenuButton.setAttribute('aria-expanded', 'true');

        // Focus the close button after transition
        setTimeout(function () {
            if (closeMobileMenu) closeMobileMenu.focus();
        }, 100);
    }

    function closeMobileMenuFn() {
        if (!mobileMenu) return;

        mobileMenu.classList.remove('active');
        if (mobileBackdrop) mobileBackdrop.classList.remove('active');
        document.body.classList.remove('menu-open');
        if (mobileMenuButton) mobileMenuButton.setAttribute('aria-expanded', 'false');

        // Return focus to the button that opened the menu
        if (previousFocus) {
            previousFocus.focus();
            previousFocus = null;
        }
    }

    if (mobileMenuButton) {
        mobileMenuButton.addEventListener('click', openMobileMenu);
    }

    if (closeMobileMenu) {
        closeMobileMenu.addEventListener('click', closeMobileMenuFn);
    }

    if (mobileBackdrop) {
        mobileBackdrop.addEventListener('click', closeMobileMenuFn);
    }

    // Close on Escape key
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && mobileMenu && mobileMenu.classList.contains('active')) {
            closeMobileMenuFn();
        }
    });

    // Close mobile menu when clicking on a navigation link
    if (mobileMenu) {
        mobileMenu.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', closeMobileMenuFn);
        });
    }

    // Focus trap inside mobile menu
    if (mobileMenu) {
        mobileMenu.addEventListener('keydown', function (e) {
            if (e.key !== 'Tab') return;
            if (!mobileMenu.classList.contains('active')) return;

            var focusable = mobileMenu.querySelectorAll(
                'a[href], button, [tabindex]:not([tabindex="-1"])'
            );
            if (focusable.length === 0) return;

            var first = focusable[0];
            var last = focusable[focusable.length - 1];

            if (e.shiftKey) {
                if (document.activeElement === first) {
                    e.preventDefault();
                    last.focus();
                }
            } else {
                if (document.activeElement === last) {
                    e.preventDefault();
                    first.focus();
                }
            }
        });
    }

    /* --------------------------------------------------------
       FOOTER YEAR
       -------------------------------------------------------- */
    var yearElement = document.getElementById('currentYear');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }

    /* --------------------------------------------------------
       SPLASH LOADER — every page load
       Orange bar fills, "Loading" sits at the top, status text
       cycles at the bottom, and the two plug halves meet to
       form the J before the splash fades away.
       Hides once window 'load' has fired AND the minimum
       display time has elapsed (whichever happens last).
       -------------------------------------------------------- */
    function initSplashLoader() {
        var splash = document.getElementById('jt-splash');
        if (!splash) return;

        var reduce = window.matchMedia &&
            window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        var MIN_SHOW = reduce ? 400 : 2200;
        var bar = document.getElementById('jt-splash-bar-fill');
        var statusEl = document.getElementById('jt-splash-status');
        var statuses = ['Initializing', 'Preparing', 'Almost there', 'Launching'];

        // Lock scroll while the splash is up.
        document.documentElement.classList.add('jt-loading');

        // Fill the orange bar with an ease-out curve to ~98%.
        var fillDur = MIN_SHOW * 0.92;
        var fillStart = null;
        function fillFrame(ts) {
            if (fillStart === null) fillStart = ts;
            var p = Math.min((ts - fillStart) / fillDur, 1);
            var eased = 1 - Math.pow(1 - p, 2);
            if (bar) bar.style.width = (eased * 98).toFixed(2) + '%';
            if (p < 1) window.requestAnimationFrame(fillFrame);
        }

        if (reduce) {
            if (bar) bar.style.width = '98%';
        } else {
            window.requestAnimationFrame(fillFrame);
        }

        // Cycle the bottom status text.
        var idx = 0;
        var statusTimer = null;
        if (!reduce) {
            statusTimer = window.setInterval(function () {
                idx = (idx + 1) % statuses.length;
                if (statusEl) {
                    statusEl.style.opacity = '0';
                    window.setTimeout(function () {
                        statusEl.textContent = statuses[idx];
                        statusEl.style.opacity = '1';
                    }, 240);
                }
            }, 620);
        }

        var flags = { load: document.readyState === 'complete', min: false };
        var done = false;

        function finish() {
            if (done) return;
            done = true;
            if (statusTimer) window.clearInterval(statusTimer);
            if (bar) bar.style.width = '100%';
            document.documentElement.classList.remove('jt-loading');
            splash.classList.add('is-hidden');
            window.setTimeout(function () {
                if (splash.parentNode) splash.parentNode.removeChild(splash);
            }, 600);
        }

        function attemptFinish() {
            if (flags.load && flags.min) finish();
        }

        window.setTimeout(function () { flags.min = true; attemptFinish(); }, MIN_SHOW);
        window.addEventListener('load', function () { flags.load = true; attemptFinish(); });

        // Safety net if 'load' never fires (blocked resources).
        window.setTimeout(function () {
            if (!flags.load) {
                flags.load = true;
                attemptFinish();
            }
        }, MIN_SHOW + 2000);
    }

    initSplashLoader();

    /* --------------------------------------------------------
       THEME TOGGLE
       -------------------------------------------------------- */
    function initThemeToggle() {
        var root = document.documentElement;
        var buttons = Array.prototype.slice.call(
            document.querySelectorAll('#themeToggle, #themeToggleMobile')
        );
        if (!buttons.length) return;

        function syncIcons() {
            var isDark = root.classList.contains('dark');
            document.querySelectorAll('#themeToggleIcon, #themeToggleIconMobile').forEach(function (icon) {
                icon.className = isDark ? 'fa-solid fa-sun text-sm' : 'fa-solid fa-moon text-sm';
            });
        }

        buttons.forEach(function (button) {
            button.addEventListener('click', function () {
                root.classList.toggle('dark');
                var theme = root.classList.contains('dark') ? 'dark' : 'light';
                try {
                    localStorage.setItem('theme', theme);
                } catch (e) { /* storage unavailable */ }
                syncIcons();
            });
        });

        syncIcons();
    }

    initThemeToggle();

    /* --------------------------------------------------------
       PREMIUM NAV — cinematic collapse on scroll
       --------------------------------------------------------
       JS only handles the scroll state (below the page threshold the navbar
       is fully expanded; past it, it collapses to a logo-only pill).

       Hover expansion (:hover) and keyboard expansion (:focus-within) are
       handled purely in CSS, so pointer and focus behaviour needs no JS.
       -------------------------------------------------------- */
    function initPremiumNav() {
        var navbar = document.getElementById('navbar');
        if (!navbar) return;

        var isCollapsed = false;

        var COLLAPSE_AT = 100;  // scrollY that triggers collapse
        var EXPAND_AT = 60;     // scrollY below which it expands again

        function handleScroll() {
            var y = window.scrollY || 0;
            var shouldCollapse;

            // Hysteresis band (60-100px) prevents flicker near the threshold.
            if (y > COLLAPSE_AT) {
                shouldCollapse = true;
            } else if (y < EXPAND_AT) {
                shouldCollapse = false;
            } else {
                shouldCollapse = isCollapsed;
            }

            if (shouldCollapse !== isCollapsed) {
                isCollapsed = shouldCollapse;
                navbar.classList.toggle('nav-collapsed', isCollapsed);
            }
        }

        function onScroll() {
            window.requestAnimationFrame(handleScroll);
        }

        // Scroll listener — passive, rAF-throttled for cheap reads.
        window.addEventListener('scroll', onScroll, { passive: true });

        // Re-sync after HTMX navigation (new page content swaps in).
        document.addEventListener('htmx:afterSettle', function () {
            void document.body.offsetHeight;
            handleScroll();
        });

        handleScroll();
    }

    initPremiumNav();

    /* --------------------------------------------------------
       ACTIVE NAV LINK
       -------------------------------------------------------- */
    function updateActiveNavLink() {
        var path = window.location.pathname.replace(/\/$/, '');
        document.querySelectorAll('#navbar .nav-item, #mobileMenu .nav-item').forEach(function (link) {
            link.classList.remove('active');
            var href = link.getAttribute('href');
            if (href && href !== '#' && href.replace(/\/$/, '') === path) {
                link.classList.add('active');
            }
        });
    }

    updateActiveNavLink();
    document.addEventListener('htmx:afterSwap', updateActiveNavLink);

    /* --------------------------------------------------------
       PAGE TRANSITIONS (HTMX)
       -------------------------------------------------------- */
    function initPageTransitions() {
        var contentArea = document.getElementById('content-area');
        if (!contentArea) return;

        function playEnterAnimation() {
            contentArea.classList.remove('page-transition-out');
            contentArea.classList.remove('page-transition-in');
            void contentArea.offsetWidth;
            contentArea.classList.add('page-transition-in');

            window.requestAnimationFrame(function () {
                contentArea.classList.remove('page-transition-in');
            });
        }

        document.body.addEventListener('htmx:beforeRequest', function (event) {
            if (!event.detail || !event.detail.elt || !event.detail.elt.matches('a[href]')) {
                return;
            }
            contentArea.classList.add('page-transition-out');
        });

        document.body.addEventListener('htmx:afterSwap', function () {
            playEnterAnimation();
        });

        playEnterAnimation();
    }

    initPageTransitions();

    /* --------------------------------------------------------
       FAQ ACCORDION (event delegation — survives HTMX swaps)
       -------------------------------------------------------- */
    document.addEventListener('click', function (event) {
        var button = event.target.closest('.faq-question');
        if (!button) return;

        var item = button.closest('.faq-item');
        if (!item) return;

        var answer = item.querySelector('.faq-answer');
        if (!answer) return;

        var wasOpen = !answer.classList.contains('hidden');
        var container = item.parentElement;

        // Close all open items
        container.querySelectorAll('.faq-item.open').forEach(function (openItem) {
            openItem.classList.remove('open');
            var openAnswer = openItem.querySelector('.faq-answer');
            if (openAnswer) openAnswer.classList.add('hidden');
            var openBtn = openItem.querySelector('.faq-question');
            if (openBtn) openBtn.setAttribute('aria-expanded', 'false');
        });

        if (!wasOpen) {
            item.classList.add('open');
            answer.classList.remove('hidden');
            button.setAttribute('aria-expanded', 'true');
        }
    });

    /* --------------------------------------------------------
       LANGUAGE SWITCHER (EN/FR)
       Sets a ``lang`` cookie and reloads — server-side rendering picks
       up the new language on the next page render.
       -------------------------------------------------------- */
    function initLanguageSwitcher() {
        var options = Array.prototype.slice.call(
            document.querySelectorAll('.lang-option[data-lang]')
        );
        if (!options.length) return;

        options.forEach(function (button) {
            button.addEventListener('click', function () {
                var lang = button.getAttribute('data-lang');
                var current = (document.cookie.match(/(?:^|;\s*)lang=([^;]*)/) || [])[1] || '';
                if (lang === current) return;
                document.cookie = 'lang=' + encodeURIComponent(lang) +
                    '; path=/; max-age=31536000; SameSite=Lax';
                window.location.reload();
            });
        });
    }

    initLanguageSwitcher();

    /* --------------------------------------------------------
       CUSTOM CURSOR — theme ring + dot (fine pointers only)
       -------------------------------------------------------- */
    function initCustomCursor() {
        var wrap = document.getElementById('cursor');
        if (!wrap) return;

        var fine = window.matchMedia &&
            window.matchMedia('(pointer: fine)').matches;
        var reduce = window.matchMedia &&
            window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (!fine || reduce) return;

        document.documentElement.classList.add('has-custom-cursor');

        var dot = wrap.querySelector('.cursor-dot');
        var ring = wrap.querySelector('.cursor-ring');
        if (!dot || !ring) return;

        var dotX = -100, dotY = -100, ringX = -100, ringY = -100;
        var raf = null;
        var isDown = false;
        var overInteractive = false;
        var hidden = true;

        function showCursor() { hidden = false; wrap.style.opacity = '1'; }
        function hideCursor() { hidden = true; wrap.style.opacity = '0'; }

        document.addEventListener('mousemove', function (e) {
            dotX = e.clientX;
            dotY = e.clientY;
            showCursor();
            if (!raf) raf = window.requestAnimationFrame(tick);

            var t = e.target;
            overInteractive = !!(t.closest &&
                t.closest('a, button, [role="button"], summary, input, textarea, select, label'));
            wrap.classList.toggle('is-hover', overInteractive);
        });

        document.addEventListener('mousedown', function () {
            isDown = true;
            wrap.classList.add('is-down');
        });
        document.addEventListener('mouseup', function () {
            isDown = false;
            wrap.classList.remove('is-down');
        });

        document.addEventListener('mouseleave', function () { hideCursor(); });
        document.addEventListener('mouseenter', function () { showCursor(); });
        document.documentElement.addEventListener('mouseleave', function () { hideCursor(); });
        document.documentElement.addEventListener('mouseenter', function () { showCursor(); });

        function tick() {
            if (!hidden) {
                dot.style.transform = 'translate(' + dotX + 'px,' + dotY + 'px) translate(-50%, -50%)';
                ringX += (dotX - ringX) * 0.18;
                ringY += (dotY - ringY) * 0.18;
                ring.style.transform = 'translate(' + ringX + 'px,' + ringY + 'px) translate(-50%, -50%)';
            }
            raf = null;
        }
    }

    initCustomCursor();

    /* --------------------------------------------------------
       HERO ROTATING HEADLINE (Agbedus-style changing words)
       -------------------------------------------------------- */
    var heroRotatorInterval = null;

    function initHeroRotator() {
        var heading = document.getElementById('heroRotator');
        if (!heading) return;
        var headingPhrases = heading.querySelectorAll('.hero-headline-phrase');
        var headingCount = headingPhrases.length;
        if (headingCount < 2) return;

        var eyebrow = document.getElementById('heroEyebrow');
        var eyebrowPhrases = eyebrow ? eyebrow.querySelectorAll('.hero-eyebrow-phrase') : [];
        var eyebrowCount = eyebrowPhrases.length;

        // Heading phrases are grouped by eyebrow text (e.g. the 3 "Sound…"
        // phrases go with the first eyebrow, the 3 "Professional…" phrases
        // with the second) — only one set is ever visible at a time.
        var groupSize = (eyebrowCount > 0 && headingCount % eyebrowCount === 0)
            ? headingCount / eyebrowCount
            : headingCount;

        var reduce = window.matchMedia &&
            window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        if (heroRotatorInterval) {
            clearInterval(heroRotatorInterval);
            heroRotatorInterval = null;
        }

        var index = 0;

        function show(i) {
            headingPhrases.forEach(function (phrase, n) {
                var active = n === i;
                phrase.classList.toggle('is-active', active);
                phrase.setAttribute('aria-hidden', active ? 'false' : 'true');
            });
            var eye = groupSize > 0 ? Math.floor(i / groupSize) : -1;
            eyebrowPhrases.forEach(function (phrase, n) {
                var active = n === eye;
                phrase.classList.toggle('is-active', active);
                phrase.setAttribute('aria-hidden', active ? 'false' : 'true');
            });
        }

        if (!reduce) {
            heroRotatorInterval = setInterval(function () {
                index = (index + 1) % headingCount;
                show(index);
            }, 4000);
        } else {
            show(0);
        }
    }

    /* --------------------------------------------------------
       BY THE NUMBERS — reveal + count-up
       -------------------------------------------------------- */
    function animateCount(el) {
        var target = parseInt(el.getAttribute('data-count'), 10);
        if (isNaN(target)) return;
        var duration = 1500;
        var start = null;

        function frame(ts) {
            if (start === null) start = ts;
            var p = Math.min((ts - start) / duration, 1);
            var eased = 1 - Math.pow(1 - p, 3);
            el.textContent = Math.round(eased * target);
            if (p < 1) requestAnimationFrame(frame);
        }

        requestAnimationFrame(frame);
    }

    function initStatsSection() {
        var panel = document.getElementById('statsPanel');
        if (!panel) return;

        function reveal() {
            panel.classList.add('stats-is-visible');
            panel.querySelectorAll('.stat-num[data-count]').forEach(function (el) {
                if (el.getAttribute('data-animate') === 'false') return;
                animateCount(el);
            });
        }

        if (!('IntersectionObserver' in window)) {
            reveal();
            return;
        }

        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    reveal();
                    observer.disconnect();
                }
            });
        }, { threshold: 0.25 });

        observer.observe(panel);
    }

    initHeroRotator();
    initStatsSection();
    document.addEventListener('htmx:afterSwap', initHeroRotator);
    document.addEventListener('htmx:afterSwap', initStatsSection);

    /* --------------------------------------------------------
       FOOTER MEGA TEXT — cursor-follow parallax
       The giant "Just Tech" background word shifts slightly toward
       where the pointer is over the footer (works in light + dark).
       -------------------------------------------------------- */
    function initFooterMegaText() {
        var footer = document.querySelector('footer[role="contentinfo"]');
        var mega = footer ? footer.querySelector('.footer-mega-text') : null;
        if (!footer || !mega) return;

        var reduce = window.matchMedia &&
            window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (reduce) return;

        var MAX_X = 16;
        var MAX_Y = 12;

        var targetX = 0, targetY = 0;
        var curX = 0, curY = 0;
        var raf = null;

        function onMove(e) {
            var rect = footer.getBoundingClientRect();
            var nx = ((e.clientX - rect.left) / rect.width) - 0.5;
            var ny = ((e.clientY - rect.top) / rect.height) - 0.5;
            targetX = nx * 2 * MAX_X;
            targetY = ny * 2 * MAX_Y;
            if (!raf) raf = window.requestAnimationFrame(tick);
        }

        function onLeave() {
            targetX = 0;
            targetY = 0;
            if (!raf) raf = window.requestAnimationFrame(tick);
        }

        function tick() {
            curX += (targetX - curX) * 0.12;
            curY += (targetY - curY) * 0.12;
            mega.style.transform = 'translate(' + curX.toFixed(2) + 'px,' + curY.toFixed(2) + 'px)';
            if (Math.abs(targetX - curX) > 0.05 || Math.abs(targetY - curY) > 0.05) {
                raf = window.requestAnimationFrame(tick);
            } else {
                raf = null;
            }
        }

        footer.addEventListener('mousemove', onMove, { passive: true });
        footer.addEventListener('mouseleave', onLeave);
    }

    initFooterMegaText();
/* --------------------------------------------------------
    LOCATION — "Where we're based" (Barrie, Ontario)
            Mirrors the Agbedus brand-photo moment: the section is
            pinned while the reader scrolls, a single drawing head
            traces the outline of Canada, the locator (ring + dot)
            lands on Barrie, the coordinates and region appear, the
            plate holds, then the outline unwinds. A curtain reveals
            the real Barrie photograph and JUST TECH settles over it.
            The "Scroll" lanyard doubles as scrub progress and plays
            the whole sequence when clicked. Dependency-free (rAF).
            -------------------------------------------------------- */
    var jtLocControllers = [];

    function jtLocEaseOut(p) {
        return 1 - Math.pow(1 - p, 3);
    }

    function jtLocEaseInOut(p) {
        return p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
    }

    function jtLocClamp(v, a, b) {
        return v < a ? a : (v > b ? b : v);
    }

    function jtLocLerp(a, b, p) {
        return a + (b - a) * p;
    }

    // Eased, clamped local progress for a phase window [a, b] of p in [0, 1].
    function jtLocPhase(p, a, b) {
        if (b <= a) return 0;
        return jtLocEaseOut(jtLocClamp((p - a) / (b - a), 0, 1));
    }

    // Back-out ease: pops past 1 then settles — used for the locator dot.
    function jtLocEaseOutBack(x) {
        var c1 = 1.70158, c3 = c1 + 1;
        return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2);
    }

    // Split a closed "M…L…Z" path into ring polylines (with implicit closing edge).
    function jtLocParseRings(d) {
        var rings = [], parts = d.split('Z');
        for (var i = 0; i < parts.length; i++) {
            var part = parts[i].trim();
            if (!part) continue;
            var pts = [], m = /([ML])\s*(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)/g, mo;
            while ((mo = m.exec(part)) !== null) {
                if (mo[1] === 'M' && pts.length) break;
                pts.push([parseFloat(mo[2]), parseFloat(mo[3])]);
            }
            if (pts.length < 3) continue;
            var seq = pts.concat([pts[0]]);
            var cum = [0], len = 0;
            for (var j = 0; j < seq.length - 1; j++) {
                var dx = seq[j + 1][0] - seq[j][0];
                var dy = seq[j + 1][1] - seq[j][1];
                len += Math.sqrt(dx * dx + dy * dy);
                cum.push(len);
            }
            rings.push({ pts: pts, seq: seq, cum: cum, len: len });
        }
        return rings;
    }

    function jtLocPointAlong(a, b, edgeLen, dist) {
        if (edgeLen <= 0) return a;
        var f = dist / edgeLen;
        return [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f];
    }

    // Rebuild the trace 'd' for the whole [startD, endD] arc of the outline.
    function jtLocTraceRings(rings, startD, endD) {
        var parts = [];
        for (var i = 0; i < rings.length; i++) {
            var ring = rings[i];
            var rs = ring.start;
            var re = rs + ring.len;
            if (startD >= re - 0.001 || endD <= rs + 0.001) continue;

            // Fully inside the window: emit the closed ring as stored.
            if (startD <= rs + 0.001 && endD >= re - 0.001) {
                parts.push('M' + ring.pts[0][0].toFixed(1) + ' ' + ring.pts[0][1].toFixed(1));
                for (var j = 1; j < ring.pts.length; j++) {
                    parts.push('L' + ring.pts[j][0].toFixed(1) + ' ' + ring.pts[j][1].toFixed(1));
                }
                parts.push('Z');
                continue;
            }

            // Partial ring: clip the closed sequence to the window.
            var lo = Math.max(0, startD - rs);
            var hi = Math.min(ring.len, endD - rs);
            for (var k = 0; k < ring.seq.length - 1; k++) {
                var c0 = ring.cum[k];
                var c1 = ring.cum[k + 1];
                if (c1 <= lo || c0 >= hi) continue;
                var f0 = Math.max(c0, lo);
                var f1 = Math.min(c1, hi);
                var p0 = jtLocPointAlong(ring.seq[k], ring.seq[k + 1], c1 - c0, f0 - c0);
                var p1 = jtLocPointAlong(ring.seq[k], ring.seq[k + 1], c1 - c0, f1 - c0);
                if (!parts.length) {
                    parts.push('M' + p0[0].toFixed(1) + ' ' + p0[1].toFixed(1));
                } else {
                    parts.push('L' + p0[0].toFixed(1) + ' ' + p0[1].toFixed(1));
                }
                parts.push('L' + p1[0].toFixed(1) + ' ' + p1[1].toFixed(1));
            }
        }
        return parts.join('');
    }

    function initLocationSection() {
        var sections = document.querySelectorAll('[data-jt-loc]');
        if (!sections.length) return;

        var reduce = window.matchMedia &&
            window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        Array.prototype.forEach.call(sections, function (section) {
            if (section.getAttribute('data-jt-loc-inited') !== null) return;
            section.setAttribute('data-jt-loc-inited', 'true');

            var $ = function (sel) { return section.querySelector(sel); };
            var stage = $('[data-jt-stage]');
            var grid = $('[data-jt-grid]');
            var scan = $('[data-jt-scan]');
            var map = $('[data-jt-map]');
            var caPath = $('[data-jt-canada]');
            var dot = $('[data-jt-dot]');
            var ring = $('[data-jt-ring]');
            var label = $('[data-jt-label]');
            var meta = $('[data-jt-meta]');
            var unity = $('[data-jt-unity]');
            var photo = $('[data-jt-photo]');
            var photoInner = $('[data-jt-photo-inner]');
            var photoImg = $('[data-jt-photo-img]');
            var brand = $('[data-jt-brand]');
            var letters = brand ? brand.querySelectorAll('.jt-brand-letter') : null;
            var tagWords = brand ? brand.querySelectorAll('.jt-tag-word') : null;
            var source = $('[data-jt-map-source]');
            var credits = $('[data-jt-credits]');
            var cue = $('[data-jt-cue]');
            var cueFill = $('[data-jt-cue-fill]');

            // Parse the Canada outline into rings; assign global offsets.
            var rings = [];
            var totalLen = 0;
            if (caPath) {
                rings = jtLocParseRings(caPath.getAttribute('d'));
                for (var ri = 0; ri < rings.length; ri++) {
                    rings[ri].start = totalLen;
                    totalLen += rings[ri].len;
                }
            }

            // Timeline windows (normalized over the pinned travel).
            var T = {
                stageIn:   { a: 0.000, b: 0.035 },
                gridIn:    { a: 0.000, b: 0.060 },
                scanSweep: { a: 0.050, b: 0.200 },
                scanOut:   { a: 0.340, b: 0.400 },
                draw:      { a: 0.055, b: 0.300 },
                hold:      { a: 0.300, b: 0.420 },
                metaIn:    { a: 0.300, b: 0.360 },
                dotIn:     { a: 0.315, b: 0.355 },
                ping:      { a: 0.340, b: 0.430 },
                labelIn:   { a: 0.360, b: 0.430 },
                push:      { a: 0.460, b: 0.600 },
                exit:      { a: 0.680, b: 0.860 },
                gridOut:   { a: 0.800, b: 0.880 },
                stageOut:  { a: 0.840, b: 0.920 },
                curtain:   { a: 0.885, b: 1.000 },
                letters:   { a: 0.930, b: 1.000 },
                creditsIn: { a: 0.900, b: 0.960 }
            };

            function render(p) {
                var phase, lp;

                if (stage) {
                    stage.style.opacity = (
                        jtLocPhase(p, T.stageIn.a, T.stageIn.b) *
                        (1 - jtLocPhase(p, T.stageOut.a, T.stageOut.b))
                    ).toFixed(3);
                }

                if (grid) {
                    phase = jtLocPhase(p, T.push.a, T.push.b);
                    grid.style.transform = 'scale(' + (1 + 0.3 * phase).toFixed(4) + ')';
                    grid.style.opacity = (
                        jtLocPhase(p, T.gridIn.a, T.gridIn.b) *
                        (1 - jtLocPhase(p, T.gridOut.a, T.gridOut.b)) *
                        (1 - 0.3 * phase)
                    ).toFixed(3);
                }

                if (scan) {
                    scan.style.transform = 'translateX(' +
                        jtLocLerp(-60, 60, jtLocPhase(p, T.scanSweep.a, T.scanSweep.b)).toFixed(2) + '%)';
                    scan.style.opacity = (
                        jtLocPhase(p, T.scanSweep.a, T.scanSweep.a + 0.02) *
                        (1 - jtLocPhase(p, T.scanOut.a, T.scanOut.b))
                    ).toFixed(3);
                }

                // Canada outline: drawing head builds, plateau holds, unwinds.
                if (caPath && rings.length) {
                    var end = totalLen * jtLocPhase(p, T.draw.a, T.draw.b);
                    var start = totalLen * jtLocPhase(p, T.exit.a, T.exit.a + 0.94 * (T.exit.b - T.exit.a));
                    caPath.setAttribute('d', jtLocTraceRings(rings, start, end));
                }

                // Camera push-in on the map.
                if (map) {
                    map.style.transform = 'scale(' +
                        (1 + 0.16 * jtLocPhase(p, T.push.a, T.push.b)).toFixed(4) + ')';
                }

                // Coordinates under the map.
                if (meta) {
                    phase = jtLocPhase(p, T.metaIn.a, T.metaIn.b);
                    meta.style.opacity = (phase * (1 - jtLocPhase(p, T.exit.a, T.exit.a + 0.08))).toFixed(3);
                    meta.style.transform = 'translateY(' + (8 * (1 - phase)).toFixed(2) + 'px)';
                }

                // Map source: slides in once the coordinates are up, leaves later.
                if (source) {
                    var srcIn = jtLocPhase(p, T.metaIn.a + 0.03, T.metaIn.b + 0.03);
                    source.style.opacity = (srcIn * (1 - jtLocPhase(p, T.exit.a, T.exit.a + 0.08))).toFixed(3);
                    source.style.transform = 'translateY(' + (6 * (1 - srcIn)).toFixed(2) + 'px)';
                }

                // "Barrie" label rises over the dot.
                if (label) {
                    phase = jtLocPhase(p, T.labelIn.a, T.labelIn.b);
                    label.style.opacity = (phase * (1 - jtLocPhase(p, T.exit.a, T.exit.a + 0.10))).toFixed(3);
                    label.style.transform = 'translateY(' + ((1 - phase) * 14).toFixed(2) + 'px)';
                }

                // Locator dot pops in (back-ease) and leaves with the exit.
                if (dot) {
                    var dotIn = jtLocPhase(p, T.dotIn.a, T.dotIn.b);
                    dot.style.opacity = (dotIn * (1 - jtLocPhase(p, T.exit.a, T.exit.a + 0.12))).toFixed(3);
                    dot.style.transform = 'scale(' +
                        (0.2 * (1 - dotIn) + jtLocEaseOutBack(dotIn)).toFixed(3) + ')';
                }

                // Ring ping: one expanding pulse once the dot lands.
                if (ring) {
                    var pingP = jtLocPhase(p, T.ping.a, T.ping.b);
                    ring.style.opacity = (4 * pingP * (1 - pingP) *
                        (1 - jtLocPhase(p, T.exit.a, T.exit.a + 0.10))).toFixed(3);
                    ring.style.transform = 'scale(' + (0.35 + 2.05 * pingP).toFixed(3) + ')';
                }

                // Region chip: in with the outline, out with the exit.
                if (unity) {
                    unity.style.opacity = (
                        jtLocPhase(p, T.stageIn.a, T.stageIn.b) *
                        (1 - jtLocPhase(p, T.exit.a, T.exit.a + 0.06))
                    ).toFixed(3);
                    unity.style.transform = 'translateY(' +
                        (-6 * jtLocPhase(p, T.exit.a, T.exit.a + 0.06)).toFixed(2) + 'px)';
                }

                // Curtain reveal: photo sweeps in from the left of the pin.
                var cv = jtLocEaseInOut(jtLocPhase(p, T.curtain.a, T.curtain.b));
                if (photo) {
                    photo.style.clipPath = 'inset(0 ' + ((1 - cv) * 100).toFixed(2) + '% 0 0)';
                    photo.style.webkitClipPath = photo.style.clipPath;
                }
                if (photoInner) {
                    photoInner.style.transform = 'translateY(' + (-12 * cv).toFixed(2) + '%)';
                }
                if (photoImg) {
                    photoImg.style.filter = 'grayscale(' + (0.85 * (1 - cv)).toFixed(2) + ') contrast(1.06)';
                }

                // JUST TECH settles in letter by letter, then the tagline by word.
                if (letters && letters.length) {
                    for (var li = 0; li < letters.length; li++) {
                        lp = jtLocPhase(p, T.letters.a + li * 0.006, T.letters.a + (li + 1) * 0.006 + 0.02);
                        letters[li].style.opacity = lp.toFixed(3);
                        letters[li].style.transform = 'translateY(' + ((1 - lp) * 0.5).toFixed(3) + 'em)';
                    }
                }
                if (tagWords && tagWords.length) {
                    for (var wi = 0; wi < tagWords.length; wi++) {
                        lp = jtLocPhase(p, T.letters.a + 0.025 + wi * 0.006, T.letters.a + 0.025 + (wi + 1) * 0.006 + 0.02);
                        tagWords[wi].style.opacity = lp.toFixed(3);
                        tagWords[wi].style.transform = 'translateY(' + ((1 - lp) * 0.35).toFixed(3) + 'em)';
                    }
                }

                if (credits) {
                    credits.style.opacity = jtLocPhase(p, T.creditsIn.a, T.creditsIn.b).toFixed(3);
                }
                if (cue) {
                    cue.classList.toggle('jt-cue-on-photo', p >= T.stageOut.a);
                }
                if (cueFill) {
                    cueFill.style.width = (p * 100).toFixed(1) + '%';
                }
            }

            // Route: the lanyard click plays the whole sequence via scrolling.
            var playing = false;
            var playRaf = null;
            var playCancelled = false;

            function playCleanup() {
                var names = ['wheel', 'touchstart', 'keydown'];
                for (var ci = 0; ci < names.length; ci++) {
                    window.removeEventListener(names[ci], playCleanup);
                }
                playRaf = null;
                playing = false;
            }

            function playCancel() {
                playCancelled = true;
                if (playRaf) window.cancelAnimationFrame(playRaf);
                playCleanup();
            }

            function playScrollSequence() {
                if (playing) return;
                var y0 = window.pageYOffset || document.documentElement.scrollTop;
                var rect = section.getBoundingClientRect();
                var secTop = rect.top + y0;
                var travelY = section.offsetHeight - window.innerHeight;
                if (travelY < 1) travelY = 1;
                var begin = Math.max(y0, secTop);
                var endY = secTop + travelY;
                if (endY - begin < 1) {
                    window.scrollTo({ top: endY, behavior: 'auto' });
                    return;
                }
                var dur = reduce ? 400 : 2600;
                var st = null;
                playCancelled = false;
                playing = true;
                var names = ['wheel', 'touchstart', 'keydown'];
                for (var ci = 0; ci < names.length; ci++) {
                    window.addEventListener(names[ci], playCancel, { passive: true });
                }
                window.requestAnimationFrame(function step(ts) {
                    if (playCancelled) return;
                    if (!st) st = ts;
                    var k = jtLocClamp((ts - st) / dur, 0, 1);
                    var y = begin + (endY - begin) * jtLocEaseInOut(k);
                    window.scrollTo(0, y);
                    if (k < 1 && !playCancelled) {
                        playRaf = window.requestAnimationFrame(step);
                    } else {
                        playCleanup();
                    }
                });
            }

            if (cue) {
                cue.addEventListener('click', function (e) {
                    if (e && e.preventDefault) e.preventDefault();
                    playScrollSequence();
                });
            }

            var raf = null;
            var near = true;
            var io = null;

            function kill() {
                if (raf) window.cancelAnimationFrame(raf);
                if (io && io.disconnect) io.disconnect();
                playCancel();
                raf = null;
                near = false;
            }

            jtLocControllers.push({ section: section, kill: kill });

            // Reduced motion: skip the loop, show the final state.
            if (reduce) {
                render(1);
                return;
            }

            function frame() {
                raf = null;
                if (!near) return;
                var rect = section.getBoundingClientRect();
                var travel = rect.height - window.innerHeight;
                if (travel < 1) travel = 1;
                var p = jtLocClamp(-rect.top / travel, 0, 1);
                render(p);
                raf = window.requestAnimationFrame(frame);
            }

            if ('IntersectionObserver' in window) {
                io = new IntersectionObserver(function (entries) {
                    var any = false;
                    for (var i = 0; i < entries.length; i++) {
                        if (entries[i].isIntersecting) { any = true; break; }
                    }
                    near = any;
                    if (near && !raf) raf = window.requestAnimationFrame(frame);
                }, { rootMargin: '120% 0px 120% 0px' });
                io.observe(section);
            }

            if (near && !raf) raf = window.requestAnimationFrame(frame);
        });
    }

    // Tear down controllers whose sections were swapped out by HTMX navigation.
    function jtPruneLocatorControllers() {
        jtLocControllers = jtLocControllers.filter(function (controller) {
            if (document.body.contains(controller.section)) return true;
            controller.kill();
            return false;
        });
    }

    initLocationSection();
    document.addEventListener('htmx:afterSwap', initLocationSection);
    document.addEventListener('htmx:afterSwap', jtPruneLocatorControllers);

    /* --------------------------------------------------------
       SCROLL REVEAL — generic driver for [data-reveal].is-in
       Runs on every page; re-initialised after htmx swaps.
       -------------------------------------------------------- */
    function initReveal() {
        var els = document.querySelectorAll('[data-reveal]:not([data-reveal-bound])');
        if (!els.length) return;

        var reduce = window.matchMedia &&
            window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        // No IntersectionObserver or reduced motion: show everything at once.
        if (reduce || !('IntersectionObserver' in window)) {
            els.forEach(function (el) {
                el.classList.add('is-in');
                el.setAttribute('data-reveal-bound', '1');
            });
            return;
        }

        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;
                var el = entry.target;
                var delay = parseInt(el.getAttribute('data-reveal-delay'), 10) || 0;
                el.style.transitionDelay = delay + 'ms';
                el.classList.add('is-in');
                el.setAttribute('data-reveal-bound', '1');
                io.unobserve(el);
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

        els.forEach(function (el) { io.observe(el); });
    }

    initReveal();
    document.addEventListener('htmx:afterSwap', initReveal);

    /* --------------------------------------------------------
       CONTACT — provider sign-in buttons (UI only)
       -------------------------------------------------------- */
    function initProviderButtons() {
        var buttons = document.querySelectorAll('[data-provider]');
        var note = document.getElementById('jt-provider-note');
        var emailField = document.getElementById('jt-email');
        if (!buttons.length) return;

        function clearChoosingTimers() {
            buttons.forEach(function (b) {
                if (b.__t) { clearTimeout(b.__t); b.__t = null; }
            });
        }

        buttons.forEach(function (btn) {
            if (btn.dataset.bound === '1') return;
            btn.dataset.bound = '1';
            btn.addEventListener('click', function () {
                var provider = btn.getAttribute('data-provider');
                clearChoosingTimers();
                buttons.forEach(function (b) { b.classList.remove('is-choosing'); });
                btn.classList.add('is-choosing');
                btn.__t = setTimeout(function () {
                    btn.classList.remove('is-choosing');
                    btn.__t = null;
                }, 1400);

                if (note) {
                    var template = note.getAttribute('data-template') || '';
                    note.textContent = template.replace('__PROVIDER__', provider || '');
                    note.hidden = false;
                }
                if (emailField) {
                    emailField.classList.add('is-steered');
                    emailField.focus({ preventScroll: true });
                }
            });
        });
    }

    initProviderButtons();
    document.addEventListener('htmx:afterSwap', initProviderButtons);

    /* --------------------------------------------------------
       COOKIE CONSENT
       Stores only the visitor's consent choice. No analytics or
       advertising scripts are enabled by this site.
       -------------------------------------------------------- */
    function initCookieConsent() {
        var banner = document.getElementById('cookieConsent');
        if (!banner) return;

        var accept = document.getElementById('cookieConsentAccept');
        var decline = document.getElementById('cookieConsentDecline');

        function readChoice() {
            var match = document.cookie.match(/(?:^|;\s*)cookie_consent=([^;]*)/);
            return match ? decodeURIComponent(match[1]) : '';
        }

        function saveChoice(choice) {
            document.cookie = 'cookie_consent=' + encodeURIComponent(choice) +
                '; path=/; max-age=31536000; SameSite=Lax';
            try {
                localStorage.setItem('cookie_consent', choice);
            } catch (e) { /* storage unavailable */ }
            banner.hidden = true;
        }

        if (!readChoice()) {
            banner.hidden = false;
        }

        if (accept) {
            accept.addEventListener('click', function () {
                saveChoice('essential');
            });
        }
        if (decline) {
            decline.addEventListener('click', function () {
                saveChoice('declined');
            });
        }

        document.querySelectorAll('[data-open-cookie-preferences]').forEach(function (button) {
            button.addEventListener('click', function () {
                banner.hidden = false;
                if (accept) accept.focus();
            });
        });
    }

    initCookieConsent();
})();

