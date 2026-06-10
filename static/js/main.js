// Mobile menu functionality
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu setup
    const mobileMenuButton = document.getElementById('mobileMenuButton');
    const mobileMenu = document.getElementById('mobileMenu');
    const closeMobileMenu = document.getElementById('closeMobileMenu');
    
    if (mobileMenuButton && mobileMenu && closeMobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.add('active');
        });
        
        closeMobileMenu.addEventListener('click', () => {
            mobileMenu.classList.remove('active');
        });
        
        // Close mobile menu when clicking on a link
        const mobileLinks = mobileMenu.querySelectorAll('a');
        mobileLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.remove('active');
            });
        });
    }
    
    // Update year in footer
    const currentYear = new Date().getFullYear();
    const yearElement = document.getElementById('currentYear');
    if (yearElement) {
        yearElement.textContent = currentYear;
    }
    
    // Initialize floating nav
    initFloatingNav();

    // Replay page fade transitions after every HTMX navigation
    initPageTransitions();
    
    // Set active nav link on page load
    updateActiveNavLink();
});

// Update active nav link based on current URL
function updateActiveNavLink() {
    const path = window.location.pathname.replace(/\/$/, '');
    document.querySelectorAll('#navbar .nav-item, #mobileMenu .nav-item').forEach(link => {
        link.classList.remove('text-red-500', 'active');
        const href = link.getAttribute('href');
        if (href && href !== '#' && href.replace(/\/$/, '') === path) {
            link.classList.add('text-red-500', 'active');
        }
    });
}

// Update nav on HTMX navigation
document.addEventListener('htmx:afterSwap', updateActiveNavLink);

function initPageTransitions() {
    const contentArea = document.getElementById('content-area');

    if (!contentArea) {
        return;
    }

    const playEnterAnimation = () => {
        contentArea.classList.remove('page-transition-out');
        contentArea.classList.remove('page-transition-in');
        void contentArea.offsetWidth;
        contentArea.classList.add('page-transition-in');

        window.requestAnimationFrame(() => {
            contentArea.classList.remove('page-transition-in');
        });
    };

    document.body.addEventListener('htmx:beforeRequest', function(event) {
        if (!event.detail || !event.detail.elt || !event.detail.elt.matches('a[href]')) {
            return;
        }

        contentArea.classList.add('page-transition-out');
    });

    document.body.addEventListener('htmx:afterSwap', function() {
        playEnterAnimation();
    });

    playEnterAnimation();
}

// Hover + scroll-reveal navbar
function initFloatingNav() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    let lastScrollY = window.scrollY;
    let ticking = false;

    const showNav = () => {
        navbar.classList.remove('nav-hidden');
        navbar.classList.add('nav-visible');
    };

    const hideNav = () => {
        navbar.classList.remove('nav-visible');
        navbar.classList.add('nav-hidden');
    };

    showNav();

    const handleScroll = () => {
        const currentScrollY = window.scrollY;

        if (currentScrollY <= 0) {
            showNav();
        } else if (currentScrollY > lastScrollY) {
            hideNav();
        } else if (currentScrollY < lastScrollY) {
            showNav();
        }

        lastScrollY = currentScrollY;
    };

    const onScroll = () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                handleScroll();
                ticking = false;
            });
            ticking = true;
        }
    };

    window.addEventListener('scroll', onScroll, { passive: true });

    // Keyboard users
    const links = navbar.querySelectorAll('a');
    links.forEach(link => {
        link.addEventListener('focus', showNav);
    });

    // Re-sync nav state after HTMX page navigation
    document.addEventListener('htmx:afterSettle', function() {
        void document.body.offsetHeight;
        handleScroll();
    });

    handleScroll();
}
