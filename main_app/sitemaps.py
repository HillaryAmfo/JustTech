from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """Public, indexable pages of the site.

    Intentional exclusions:
    - booking — transactional/action page; every confirmable route variant is a
      `?service=` duplicate, which adds no search value.
    - login / logout / admin — not intended for search engines.
    - partial & API endpoints (service-price, filter_offerings,
      register-workshop, booking/contact success fragments) — HTMX/JSON only.
    """

    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return ['home', 'about', 'services', 'learning', 'portfolio', 'pricing', 'contact',
                'hire_the_band', 'book_studio', 'what_you_need', 'book_a_lesson']

    def location(self, item):
        return reverse(item)