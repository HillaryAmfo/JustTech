(function () {
    var carousel = null;

    function initTeamCarousel() {
        var wrap = document.getElementById('team-carousel');
        if (!wrap || wrap.dataset.carouselInit === '1') return;
        wrap.dataset.carouselInit = '1';

        var IS_FR = (document.documentElement.lang || '').toLowerCase().indexOf('fr') === 0;

        var cards = Array.prototype.slice.call(wrap.querySelectorAll('.team-card'));
        var dotsWrap = document.getElementById('team-dots');
        var nameEl = document.getElementById('team-name');
        var roleEl = document.getElementById('team-role');
        var bioEl = document.getElementById('team-bio');
        var imgEl = document.getElementById('team-img');
        var initialsEl = document.getElementById('team-img-initials');
        var avatarEl = document.getElementById('team-image');
        var socialLinks = document.querySelectorAll('.team-caption__social a');
        var upArrows = document.querySelectorAll('.team-arrow-up');
        var downArrows = document.querySelectorAll('.team-arrow-down');
        var count = cards.length;

        if (!count || !dotsWrap || !nameEl || !roleEl || !bioEl) return;

        var currentIndex = 0;
        var isAnimating = false;

        var team = cards.map(function (card) {
            var photo = card.querySelector('.team-avatar__img');
            return {
                name: card.dataset.name || '',
                role: IS_FR ? (card.dataset.frRole || card.dataset.role || '') : (card.dataset.role || ''),
                bio: IS_FR ? (card.dataset.frBio || card.dataset.bio || '') : (card.dataset.bio || ''),
                src: photo ? (photo.src || '') : '',
                alt: photo ? (photo.alt || '') : '',
                linkedin: card.dataset.linkedin || '#',
                instagram: card.dataset.instagram || '#'
            };
        });

        team.forEach(function (member) {
            if (member.src) {
                var preload = new Image();
                preload.src = member.src;
            }
        });

        function setImage(i) {
            var member = team[i];
            if (!imgEl) return;
            imgEl.style.opacity = '0';
            setTimeout(function () {
                if (member.src) {
                    imgEl.src = member.src;
                    imgEl.alt = member.alt || member.name || '';
                    imgEl.style.display = '';
                    if (initialsEl) initialsEl.style.display = 'none';
                } else {
                    imgEl.removeAttribute('src');
                    imgEl.style.display = 'none';
                    if (initialsEl) {
                        initialsEl.textContent = (member.name || '?').split(/\s+/).map(function (w) {
                            return w.charAt(0);
                        }).join('').slice(0, 2).toUpperCase();
                        initialsEl.style.display = '';
                    }
                }
                imgEl.style.opacity = '1';
            }, 150);
            if (socialLinks && socialLinks[0]) socialLinks[0].href = member.linkedin;
            if (socialLinks && socialLinks[1]) socialLinks[1].href = member.instagram;
        }

        function sizeAvatar() {
            if (!avatarEl || !nameEl) return;
            var w = nameEl.getBoundingClientRect().width;
            if (!w) return;
            avatarEl.style.width = Math.max(240, Math.min(w, 560)).toFixed(0) + 'px';
        }

        var dots = cards.map(function (card, i) {
            var dot = document.createElement('button');
            dot.type = 'button';
            dot.setAttribute('aria-label', 'Go to ' + (team[i].name || ('member ' + (i + 1))));
            dot.style.width = '12px';
            dot.style.height = '12px';
            dot.style.borderRadius = '9999px';
            dot.style.cursor = 'pointer';
            dot.style.transition = 'all 300ms ease';
            dot.style.backgroundColor = 'rgba(255, 0, 60, 0.2)';
            dot.addEventListener('click', function () { updateCarousel(i); });
            dotsWrap.appendChild(dot);
            return dot;
        });

        wrap.addEventListener('click', function (e) {
            var card = e.target && e.target.closest ? e.target.closest('.team-card') : null;
            if (!card) return;
            var index = cards.indexOf(card);
            if (index === -1) return;
            if (index === currentIndex) {
                updateCarousel((currentIndex + 1) % count);
            } else {
                updateCarousel(index);
            }
        });

        cards.forEach(function (card, i) {
            card.addEventListener('mouseenter', function () { setImage(i); });
            card.addEventListener('mouseleave', function () { setImage(currentIndex); });
        });

        function isMobile() {
            return window.innerWidth < 768;
        }

        function yShift(multiplier) {
            var step = isMobile() ? 80 : 150;
            return (multiplier * step) + 'px';
        }

        function stateFor(offset) {
            var gs = 'grayscale(100%)';
            var centerScale = isMobile() ? '1.08' : '1.18';
            if (offset === 0) return { transform: 'scale(' + centerScale + ') translateZ(0)', opacity: '1', filter: 'none', zIndex: 10, pe: 'auto' };
            if (offset === 1) return { transform: 'translateY(' + yShift(1) + ') scale(0.9) translateZ(-100px)', opacity: '0.9', filter: gs, zIndex: 5, pe: 'auto' };
            if (offset === 2) return { transform: 'translateY(' + yShift(2) + ') scale(0.8) translateZ(-300px)', opacity: '0.7', filter: gs, zIndex: 1, pe: 'auto' };
            if (offset === count - 1) return { transform: 'translateY(' + yShift(-1) + ') scale(0.9) translateZ(-100px)', opacity: '0.9', filter: gs, zIndex: 5, pe: 'auto' };
            if (offset === count - 2) return { transform: 'translateY(' + yShift(-2) + ') scale(0.8) translateZ(-300px)', opacity: '0.7', filter: gs, zIndex: 1, pe: 'auto' };
            return { transform: 'none', opacity: '0', filter: gs, zIndex: 0, pe: 'none' };
        }

        function applyState() {
            cards.forEach(function (card, i) {
                var offset = (i - currentIndex + count) % count;
                var s = stateFor(offset);
                card.style.transform = s.transform;
                card.style.opacity = s.opacity;
                card.style.zIndex = s.zIndex;
                card.style.pointerEvents = s.pe;
                var media = card.querySelector('img') || card.querySelector('.team-avatar');
                if (media) media.style.filter = s.filter;
            });

            dots.forEach(function (dot, i) {
                var active = i === currentIndex;
                dot.style.backgroundColor = active ? '#ff003c' : 'rgba(255, 0, 60, 0.2)';
                dot.style.transform = active ? 'scale(1.2)' : 'scale(1)';
            });
        }

        function updateCarousel(newIndex) {
            if (isAnimating) return;
            isAnimating = true;

            currentIndex = (newIndex + count) % count;
            applyState();

            nameEl.style.opacity = '0';
            roleEl.style.opacity = '0';
            bioEl.style.opacity = '0';

            setTimeout(function () {
                nameEl.textContent = team[currentIndex].name;
                roleEl.textContent = team[currentIndex].role;
                bioEl.textContent = team[currentIndex].bio;
                setImage(currentIndex);
                sizeAvatar();
                nameEl.style.opacity = '1';
                roleEl.style.opacity = '1';
                bioEl.style.opacity = '1';
            }, 300);

            setTimeout(function () {
                isAnimating = false;
            }, 800);
        }

        upArrows.forEach(function (arrow) {
            arrow.addEventListener('click', function () { updateCarousel(currentIndex - 1); });
        });

        downArrows.forEach(function (arrow) {
            arrow.addEventListener('click', function () { updateCarousel(currentIndex + 1); });
        });

        document.querySelectorAll('.team-arrow-prev').forEach(function (arrow) {
            arrow.addEventListener('click', function () { updateCarousel(currentIndex - 1); });
        });

        document.querySelectorAll('.team-arrow-next').forEach(function (arrow) {
            arrow.addEventListener('click', function () { updateCarousel(currentIndex + 1); });
        });

        carousel = {
            prev: function () { updateCarousel(currentIndex - 1); },
            next: function () { updateCarousel(currentIndex + 1); },
            apply: applyState,
            resizeAvatar: sizeAvatar
        };

        updateCarousel(0);

        if (document.fonts && document.fonts.ready) {
            document.fonts.ready.then(sizeAvatar);
        }
    }

    document.addEventListener('keydown', function (e) {
        if (!carousel) return;
        if (e.key === 'ArrowUp') carousel.prev();
        if (e.key === 'ArrowDown') carousel.next();
    });

    document.addEventListener('touchstart', function (e) {
        if (!carousel) return;
        carousel.touchStartY = e.changedTouches[0].screenY;
    }, { passive: true });

    document.addEventListener('touchend', function (e) {
        if (!carousel) return;
        var diff = carousel.touchStartY - e.changedTouches[0].screenY;
        if (Math.abs(diff) > 50) {
            if (diff > 0) carousel.next();
            else carousel.prev();
        }
    });

    window.addEventListener('resize', function () {
        if (carousel) carousel.apply();
        if (carousel && carousel.resizeAvatar) carousel.resizeAvatar();
    });

    document.addEventListener('DOMContentLoaded', initTeamCarousel);
    document.addEventListener('htmx:afterSwap', initTeamCarousel);
    initTeamCarousel();
})();
