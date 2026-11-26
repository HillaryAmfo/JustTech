(function () {
    'use strict';

    var prefersReducedMotion = window.matchMedia &&
        window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function pauseAutoplayVideos() {
        if (!prefersReducedMotion) return;
        document.querySelectorAll('video.autoplay-motion').forEach(function (video) {
            video.pause();
            video.removeAttribute('autoplay');
        });
    }

    document.addEventListener('DOMContentLoaded', pauseAutoplayVideos);
    document.addEventListener('htmx:afterSwap', pauseAutoplayVideos);
    pauseAutoplayVideos();
})();
