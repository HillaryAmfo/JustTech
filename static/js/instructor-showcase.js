(function () {
    var track = document.querySelector('[data-jt-inst-track]');
    if (!track) return;

    var section = track.closest('[data-jt-inst]');
    var cards = Array.prototype.slice.call(track.querySelectorAll('[data-jt-inst-card]'));
    var nav = document.querySelector('[data-jt-inst-nav]');
    if (!section || !nav || cards.length < 2) return;

    var previous = nav.querySelector('[data-jt-inst-prev]');
    var next = nav.querySelector('[data-jt-inst-next]');
    var playback = nav.querySelector('[data-jt-inst-playback]');
    var position = nav.querySelector('[data-jt-inst-position]');
    var progress = nav.querySelector('[data-jt-inst-progress]');
    if (!previous || !next || !playback || !position || !progress) return;

    var motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    var current = 0;
    var touchStart = null;
    var timer = null;
    var manuallyPaused = motionQuery.matches;
    var hovered = false;
    var focused = false;
    var visible = true;

    function pad(value) {
        return value < 10 ? '0' + value : String(value);
    }

    function distanceFrom(index) {
        var distance = (index - current + cards.length) % cards.length;
        if (distance > cards.length / 2) distance -= cards.length;
        return distance;
    }

    function isPaused() {
        return manuallyPaused || hovered || focused || !visible || document.hidden;
    }

    function syncPlayback() {
        var paused = isPaused();
        var label = paused ? playback.getAttribute('data-label-play') : playback.getAttribute('data-label-pause');
        var icon = playback.querySelector('i');
        playback.setAttribute('aria-label', label || 'Start autoplay');
        playback.setAttribute('aria-pressed', String(!paused));
        position.setAttribute('aria-live', paused ? 'polite' : 'off');
        if (icon) {
            icon.classList.toggle('fa-pause', !paused);
            icon.classList.toggle('fa-play', paused);
        }
    }

    function stopAutoplay() {
        if (timer !== null) {
            window.clearInterval(timer);
            timer = null;
        }
        syncPlayback();
    }

    function scheduleAutoplay() {
        stopAutoplay();
        if (isPaused()) return;
        timer = window.setInterval(function () {
            go(current + 1);
        }, 5000);
        syncPlayback();
    }

    function render(animate) {
        var width = cards[0].offsetWidth;
        track.style.height = cards[0].offsetHeight + 44 + 'px';
        track.classList.toggle('is-instant', !animate || motionQuery.matches);

        cards.forEach(function (card, index) {
            var distance = distanceFrom(index);
            var active = distance === 0;
            var neighbour = Math.abs(distance) === 1;
            var shown = active || neighbour;

            card.classList.toggle('is-active', active);
            card.classList.toggle('is-neighbour', neighbour);
            card.setAttribute('aria-hidden', String(!active));
            card.style.zIndex = active ? '3' : neighbour ? '2' : '1';
            card.style.transform = 'translate(-50%, -50%) translateX(' + distance * width * 0.67 + 'px) scale(' + (active ? 1 : 0.82) + ')';
            card.style.opacity = active ? '1' : neighbour ? '0.27' : '0';
            card.style.visibility = shown ? 'visible' : 'hidden';

            if ('inert' in card) card.inert = !shown;
            card.querySelectorAll('a, button').forEach(function (element) {
                element.tabIndex = active ? 0 : -1;
            });
        });

        position.textContent = pad(current + 1) + ' / ' + pad(cards.length);
        progress.style.transform = 'scaleX(' + ((current + 1) / cards.length) + ')';

        if (!animate || motionQuery.matches) {
            window.requestAnimationFrame(function () {
                track.classList.remove('is-instant');
            });
        }
    }

    function go(index) {
        if (cards[current].contains(document.activeElement)) {
            try {
                track.focus({ preventScroll: true });
            } catch (error) {
                track.focus();
            }
        }
        current = (index + cards.length) % cards.length;
        render(true);
        scheduleAutoplay();
    }

    cards.forEach(function (card, index) {
        card.setAttribute('role', 'group');
        card.setAttribute('aria-roledescription', 'slide');
        card.setAttribute('aria-label', pad(index + 1) + ' / ' + pad(cards.length) + ': ' + (card.getAttribute('data-jt-inst-name') || ''));
    });

    previous.addEventListener('click', function () {
        go(current - 1);
    });

    next.addEventListener('click', function () {
        go(current + 1);
    });

    playback.addEventListener('click', function () {
        manuallyPaused = !manuallyPaused;
        scheduleAutoplay();
    });

    section.addEventListener('pointerenter', function () {
        hovered = true;
        stopAutoplay();
    });

    section.addEventListener('pointerleave', function () {
        hovered = false;
        scheduleAutoplay();
    });

    section.addEventListener('focusin', function () {
        focused = true;
        stopAutoplay();
    });

    section.addEventListener('focusout', function () {
        window.setTimeout(function () {
            if (!section.contains(document.activeElement)) {
                focused = false;
                scheduleAutoplay();
            }
        }, 0);
    });

    track.addEventListener('keydown', function (event) {
        if (event.target !== track) return;
        if (event.key === 'ArrowRight') {
            event.preventDefault();
            go(current + 1);
        } else if (event.key === 'ArrowLeft') {
            event.preventDefault();
            go(current - 1);
        } else if (event.key === 'Home') {
            event.preventDefault();
            go(0);
        } else if (event.key === 'End') {
            event.preventDefault();
            go(cards.length - 1);
        }
    });

    track.addEventListener('click', function (event) {
        var card = event.target.closest('[data-jt-inst-card]');
        if (!card || card === cards[current]) return;
        var index = cards.indexOf(card);
        if (Math.abs(distanceFrom(index)) === 1) {
            event.preventDefault();
            go(index);
        }
    });

    track.addEventListener('touchstart', function (event) {
        touchStart = {
            x: event.changedTouches[0].clientX,
            y: event.changedTouches[0].clientY
        };
    }, { passive: true });

    track.addEventListener('touchend', function (event) {
        if (!touchStart) return;
        var deltaX = event.changedTouches[0].clientX - touchStart.x;
        var deltaY = event.changedTouches[0].clientY - touchStart.y;
        touchStart = null;
        if (Math.abs(deltaX) > 50 && Math.abs(deltaX) > Math.abs(deltaY) * 1.2) {
            go(current + (deltaX < 0 ? 1 : -1));
        }
    }, { passive: true });

    document.addEventListener('visibilitychange', function () {
        if (document.hidden) stopAutoplay();
        else scheduleAutoplay();
    });

    if ('IntersectionObserver' in window) {
        var observer = new IntersectionObserver(function (entries) {
            visible = entries[0].isIntersecting;
            if (visible) scheduleAutoplay();
            else stopAutoplay();
        }, { threshold: [0, 0.3] });
        observer.observe(track);
    }

    if (typeof motionQuery.addEventListener === 'function') {
        motionQuery.addEventListener('change', function () {
            manuallyPaused = motionQuery.matches;
            render(false);
            scheduleAutoplay();
        });
    } else if (typeof motionQuery.addListener === 'function') {
        motionQuery.addListener(function () {
            manuallyPaused = motionQuery.matches;
            render(false);
            scheduleAutoplay();
        });
    }

    if ('ResizeObserver' in window) {
        new ResizeObserver(function () {
            render(false);
        }).observe(cards[0]);
    } else {
        window.addEventListener('resize', function () {
            render(false);
        });
    }

    nav.hidden = false;
    track.classList.add('is-carousel');
    render(false);
    scheduleAutoplay();
})();
