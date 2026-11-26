from unittest.mock import patch

from django.conf import settings
from django.contrib.auth.models import User
from django.core.checks import run_checks
from django.db import DatabaseError
from django.template.loader import render_to_string
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from .context_processors import site_settings
from .forms import BookingForm, ContactForm
from .models import (
    Booking,
    ContactMessage,
    FAQ,
    LearningOffering,
    PortfolioItem,
    Service,
    SiteSettings,
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
        ('privacy_policy', 'main_app/privacy_policy.html'),
        ('terms', 'main_app/terms.html'),
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


class PrivacyAndTermsTests(TestCase):
    def test_privacy_policy_renders_and_is_indexable(self):
        response = self.client.get(reverse('privacy_policy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/privacy_policy.html')
        self.assertContains(response, 'Privacy Policy')
        self.assertContains(response, 'cookieConsent')

    def test_terms_renders_and_is_indexable(self):
        response = self.client.get(reverse('terms'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/terms.html')
        self.assertContains(response, 'Terms')
        self.assertContains(response, 'Conditions')

    def test_public_pages_do_not_render_secret_key(self):
        for url_name in ('privacy_policy', 'terms', 'home'):
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                content = response.content.decode()
                self.assertNotIn(settings.SECRET_KEY, content)


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


class ErrorPageTests(TestCase):
    ERROR_TEMPLATES = ('400.html', '403.html', '404.html', '500.html')

    def test_custom_404_page_content(self):
        response = self.client.get('/services/this-page-is-missing/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')
        self.assertContains(response, 'err-wrap', status_code=404)
        self.assertContains(response, 'noindex, nofollow', status_code=404)
        self.assertContains(response, '/services/this-page-is-missing/', status_code=404)
        self.assertContains(response, 'See all services', status_code=404)

    def test_all_error_templates_render(self):
        for template_name in self.ERROR_TEMPLATES:
            with self.subTest(template=template_name):
                html = render_to_string(template_name, {'request_path': '/services/missing/'})
                self.assertIn('err-wrap', html)
                self.assertIn('noindex, nofollow', html)
                self.assertIn('css/error.css', html)
                self.assertIn('err-scope', html)

    def test_site_settings_context_survives_database_error(self):
        request = RequestFactory().get('/')
        with patch.object(type(SiteSettings.objects), 'first', side_effect=DatabaseError('db down')):
            context = site_settings(request)
        self.assertIsNone(context['site_settings'])
        self.assertIn('SITE_URL', context)


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

    def test_post_login_redirect_accepts_local_next(self):
        response = self.client.post(reverse('login'), {
            'username': 'admin',
            'password': 'secret-pass',
            'next': reverse('services'),
        })
        self.assertRedirects(response, reverse('services'))

    def test_post_login_redirect_rejects_external_next(self):
        for next_url in ('https://evil.example/', '//evil.example/'):
            with self.subTest(next_url=next_url):
                self.client.logout()
                response = self.client.post(reverse('login'), {
                    'username': 'admin',
                    'password': 'secret-pass',
                    'next': next_url,
                })
                self.assertRedirects(response, reverse('home'))


class RegisterFlowTests(TestCase):
    REGISTRATION_DATA = {
        'intent': 'learning',
        'intent_detail': 'Piano',
        'full_name': 'Jane Doe',
        'email': 'jane@example.com',
        'password': 'C0mplex!Passw0rd42',
        'confirm_password': 'C0mplex!Passw0rd42',
        'agree_terms': 'on',
    }

    def test_registration_creates_user_and_profile(self):
        response = self.client.post(reverse('register'), self.REGISTRATION_DATA)
        self.assertRedirects(response, reverse('learning'))
        self.assertTrue(User.objects.filter(username='jane@example.com').exists())

    def test_post_register_redirect_accepts_local_next(self):
        response = self.client.post(reverse('register'), {
            **self.REGISTRATION_DATA,
            'next': reverse('services'),
        })
        self.assertRedirects(response, reverse('services'))

    def test_post_register_redirect_rejects_external_next(self):
        for next_url in ('https://evil.example/', '//evil.example/'):
            with self.subTest(next_url=next_url):
                self.client.logout()
                User.objects.filter(username='jane@example.com').delete()
                response = self.client.post(reverse('register'), {
                    **self.REGISTRATION_DATA,
                    'next': next_url,
                })
                self.assertRedirects(response, reverse('learning'))


class DeployConfigCheckTests(TestCase):
    @override_settings(
        HTTPS_ENABLED=True,
        SECURE_SSL_REDIRECT=True,
        SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO', 'https'),
        SESSION_COOKIE_SECURE=True,
        CSRF_COOKIE_SECURE=True,
    )
    def test_https_hardening_settings_are_enabled(self):
        self.assertTrue(settings.SECURE_SSL_REDIRECT)
        self.assertEqual(
            settings.SECURE_PROXY_SSL_HEADER,
            ('HTTP_X_FORWARDED_PROTO', 'https'),
        )
        self.assertTrue(settings.SESSION_COOKIE_SECURE)
        self.assertTrue(settings.CSRF_COOKIE_SECURE)

    def test_deploy_check_flags_insecure_defaults(self):
        with override_settings(
            DEBUG=False,
            SECRET_KEY='django-insecure-dev-key-change-me',
            ALLOWED_HOSTS=['localhost', '127.0.0.1'],
        ):
            ids = [issue.id for issue in run_checks(
                tags=['security'], include_deployment_checks=True,
            )]
        self.assertIn('main_app.E001', ids)
        self.assertIn('main_app.E002', ids)

    def test_deploy_check_passes_with_production_config(self):
        with override_settings(
            DEBUG=False,
            SECRET_KEY='a-long-random-production-secret',
            ALLOWED_HOSTS=['justtech.example'],
        ):
            ids = [issue.id for issue in run_checks(
                tags=['security'], include_deployment_checks=True,
            )]
        self.assertNotIn('main_app.E001', ids)
        self.assertNotIn('main_app.E002', ids)


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

    @override_settings(DEBUG=True)
    def test_error_stylesheet_is_served_in_debug(self):
        self.reload_urlconf()
        response = self.client.get('/static/css/error.css')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/css', response['Content-Type'])

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