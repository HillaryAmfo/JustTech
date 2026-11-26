from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from .forms import BookingForm, ContactForm
from .models import (
    Booking,
    ContactMessage,
    FAQ,
    LearningOffering,
    PortfolioItem,
    Service,
    TeamMember,
    Testimonial,
    Workshop,
    WorkshopRegistration,
)


class PageRenderTests(TestCase):
    """All public pages return 200 with the correct template."""

    PUBLIC_PAGES = [
        ('home', 'main_app/index.html'),
        ('services', 'main_app/services.html'),
        ('portfolio', 'main_app/portfolio.html'),
        ('booking', 'main_app/booking.html'),
        ('pricing', 'main_app/pricing.html'),
        ('learning', 'main_app/learning.html'),
        ('about', 'main_app/about.html'),
        ('contact', 'main_app/contact.html'),
        ('login', 'main_app/login.html'),
    ]

    def test_all_public_pages_render(self):
        for url_name, template in self.PUBLIC_PAGES:
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 200, url_name)
                self.assertTemplateUsed(response, template)


class SeoMetaTests(TestCase):
    """Meta descriptions, canonical links and Open Graph tags are present."""

    def test_home_has_canonical_and_og(self):
        response = self.client.get(reverse('home'))
        content = response.content.decode()
        self.assertIn('rel="canonical"', content)
        self.assertIn('property="og:title"', content)
        self.assertIn('property="og:url"', content)
        self.assertIn('property="og:image"', content)
        self.assertIn('name="twitter:card"', content)
        self.assertIn('name="description"', content)

    def test_robot_meta_default_is_index(self):
        response = self.client.get(reverse('home'))
        self.assertIn('name="robots" content="index, follow"', response.content.decode())

    def test_login_is_noindex(self):
        response = self.client.get(reverse('login'))
        self.assertIn('name="robots" content="noindex, nofollow"', response.content.decode())


class RobotsAndSitemapTests(TestCase):
    def test_robots_txt(self):
        response = self.client.get(reverse('robots_txt'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')
        content = response.content.decode()
        self.assertIn('User-agent: *', content)
        self.assertIn('Disallow: /admin/', content)
        self.assertIn('Sitemap:', content)

    def test_sitemap_xml_lists_public_pages(self):
        response = self.client.get(reverse('django.contrib.sitemaps.views.sitemap'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        for url in ['/about/', '/services/', '/learning/', '/portfolio/', '/pricing/', '/contact/']:
            self.assertIn(f'<loc>http://testserver{url}</loc>', content)
        self.assertNotIn('/booking/', content)


class BookingFlowTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name='Consultation', slug='consultation', short_description='A chat.',
        )

    def test_get_booking_preselected_from_query_param(self):
        response = self.client.get(reverse('booking'), {'service': self.service.slug})
        form = response.context['form']
        self.assertEqual(form['service'].value(), self.service.pk)
        self.assertEqual(response.status_code, 200)

    def test_invalid_service_slug_ignored(self):
        response = self.client.get(reverse('booking'), {'service': 'does-not-exist'})
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['form']['service'].value())

    def test_valid_submission_creates_booking(self):
        response = self.client.post(reverse('booking'), {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'phone': '+1 555 000 1111',
            'company': '',
            'service': self.service.pk,
            'preferred_date': '2026-10-01',
            'preferred_time': 'morning',
            'notes': 'Please confirm.',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['submitted'])
        self.assertTrue(Booking.objects.filter(email='jane@example.com').exists())

    def test_invalid_form_does_not_create_booking(self):
        response = self.client.post(reverse('booking'), {
            'name': '',
            'email': 'not-an-email',
            'phone': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Booking.objects.exists())


class ContactFlowTests(TestCase):
    def test_valid_submission_creates_message(self):
        response = self.client.post(reverse('contact'), {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'subject': 'Project inquiry',
            'message': 'I need a streaming setup.',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['submitted'])
        self.assertTrue(ContactMessage.objects.filter(email='jane@example.com').exists())

    def test_required_field_fails(self):
        response = self.client.post(reverse('contact'), {'name': 'Jane Doe'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ContactMessage.objects.exists())


class ServicePriceEndpointTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name='Custom Build', slug='custom-build',
            short_description='A PC.', starting_price='Starting at $999',
        )

    def test_pricing_fragment_returns_price(self):
        response = self.client.get(reverse('service_price', args=[self.service.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'$999', response.content)

    def test_missing_service_is_404(self):
        response = self.client.get(reverse('service_price', args=['nope']))
        self.assertEqual(response.status_code, 404)


class LearningFlowTests(TestCase):
    def setUp(self):
        self.offering = LearningOffering.objects.create(
            title='Intro to Audio', category='audio', description='Basics.',
        )
        self.workshop = Workshop.objects.create(
            title='Mixing Workshop', date_label='Oct 1',
            duration_label='2 hours', price_label='$49', availability_label='Open',
        )

    def test_filter_all(self):
        response = self.client.get(reverse('filter_offerings', args=['all']))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Intro to Audio', response.content)

    def test_filter_by_category(self):
        response = self.client.get(reverse('filter_offerings', args=['audio']))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Intro to Audio', response.content)

    def test_filter_empty_category(self):
        response = self.client.get(reverse('filter_offerings', args=['visual']))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Intro to Audio', response.content)

    def test_registration_creates_record(self):
        response = self.client.post(
            reverse('register_workshop', args=[self.workshop.id]),
            {'name': 'Jane Doe', 'email': 'jane@example.com', 'phone': '+1 555 000 1111'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(WorkshopRegistration.objects.filter(workshop=self.workshop).exists())


class NotFoundTests(TestCase):
    def test_unknown_url_renders_404_template(self):
        response = self.client.get('/no-such-page/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')


class LoginLogoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='secret-pass')

    def test_login_redirects_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('home'))

    def test_valid_login(self):
        response = self.client.post(reverse('login'), {'username': 'admin', 'password': 'secret-pass'})
        self.assertRedirects(response, reverse('home'))

    def test_invalid_login_shows_error(self):
        response = self.client.post(reverse('login'), {'username': 'admin', 'password': 'wrong'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password.', response.content)

    def test_logout(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'))


class DebugStaticTests(TestCase):
    """The dev-only diagnostic view is registered only while DEBUG=True.

    main_app.urls decides at module import time, so reload the module (and
    clear the URL cache) inside each test to re-evaluate the guard.
    """

    @classmethod
    def reload_urlconf(cls):
        import importlib

        import just_tech.urls
        import main_app.urls

        importlib.reload(main_app.urls)
        importlib.reload(just_tech.urls)
        from django.urls import clear_url_caches

        clear_url_caches()

    @override_settings(DEBUG=True)
    def test_debug_static_available_in_debug(self):
        self.reload_urlconf()
        response = self.client.get(reverse('debug_static'))
        self.assertEqual(response.status_code, 200)

    @override_settings(DEBUG=False, ALLOWED_HOSTS=['testserver'])
    def test_debug_static_unavailable_outside_debug(self):
        self.reload_urlconf()
        response = self.client.get('/debug-static/')
        self.assertEqual(response.status_code, 404)


class ContextProcessorTests(TestCase):
    @override_settings(ALLOWED_HOSTS=['justtech.example'])
    def test_site_url_is_built_from_request(self):
        response = self.client.get(reverse('home'), HTTP_HOST='justtech.example')
        self.assertEqual(response.context['SITE_URL'], 'http://justtech.example')
        self.assertIn(b'http://justtech.example/', response.content)


class FixtureContentTests(TestCase):
    """Pages render the content that drives them."""

    def test_home_shows_featured_services(self):
        Service.objects.create(name='Streaming', slug='streaming', is_featured=True, short_description='Rigs.')
        response = self.client.get(reverse('home'))
        self.assertIn(b'Streaming', response.content)

    def test_services_page_shows_starting_price(self):
        Service.objects.create(name='Audio', slug='audio', short_description='Setups.', starting_price='$299')
        response = self.client.get(reverse('services'))
        self.assertIn(b'$299', response.content)

    def test_portfolio_page_lists_items(self):
        PortfolioItem.objects.create(
            title='Studio 1', category='audio',
            image_url='https://images.unsplash.com/photo-1', display_order=1,
        )
        response = self.client.get(reverse('portfolio'))
        self.assertIn(b'Studio 1', response.content)

    def test_pricing_page_shows_service_prices(self):
        Service.objects.create(name='Consult', slug='consult', short_description='Chat.', starting_price='$99')
        response = self.client.get(reverse('pricing'))
        self.assertIn(b'$99', response.content)

    def test_learning_page_lists_offerings_and_instructors(self):
        LearningOffering.objects.create(title='Mixing', category='audio', description='Mix better.')
        TeamMember.objects.create(name='Alex Mixwell', role='Instructor', is_instructor=True, bio='Mixer.')
        Testimonial.objects.create(category='learning', quote='Great class.', author_name='Sam')
        response = self.client.get(reverse('learning'))
        self.assertIn(b'Mixing', response.content)
        self.assertIn(b'Alex Mixwell', response.content)

    def test_about_page_lists_team(self):
        TeamMember.objects.create(name='Jordan Tech', role='Founder', bio='Builds things.')
        response = self.client.get(reverse('about'))
        self.assertIn(b'Jordan Tech', response.content)

    def test_contact_page_shows_faqs(self):
        FAQ.objects.create(category='contact', question='Do you travel?', answer='Yes.')
        response = self.client.get(reverse('contact'))
        self.assertIn(b'Do you travel?', response.content)


class FormTests(TestCase):
    def test_booking_form_fields(self):
        form = BookingForm()
        self.assertEqual(list(form.fields.keys()), [
            'name', 'email', 'phone', 'company', 'service', 'preferred_date', 'preferred_time', 'notes',
        ])

    def test_contact_form_fields(self):
        form = ContactForm()
        self.assertEqual(list(form.fields.keys()), ['name', 'email', 'subject', 'message'])