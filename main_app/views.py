from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import (
    BookingForm,
    ContactForm,
    PasswordResetRequestForm,
    RegisterForm,
    SetNewPasswordForm,
)
from .models import (
    ContactMessage,
    FAQ,
    LearningOffering,
    PortfolioItem,
    Service,
    SiteSettings,
    TeamMember,
    Testimonial,
    UserProfile,
    Workshop,
    WorkshopRegistration,
)


def home(request):
    context = {
        'services': Service.objects.all(),
        'featured_portfolio': PortfolioItem.objects.filter(is_featured=True)[:6],
        'testimonials': Testimonial.objects.all()[:3],
        'home_faqs': FAQ.objects.all()[:6],
    }
    return render(request, 'main_app/index.html', context)


def services(request):
    priority = ['event-services', 'streaming-setups']
    all_services = list(Service.objects.all())
    featured = [s for s in all_services if s.slug in priority]
    details = sorted(
        featured + [s for s in all_services if s.slug not in priority],
        key=lambda s: (priority.index(s.slug) if s.slug in priority else 99, s.display_order, s.name),
    )[:6]
    context = {
        'service_details': details,
        'faqs': FAQ.objects.filter(category='pricing')[:4],
    }
    return render(request, 'main_app/services.html', context)


def portfolio(request):
    portfolio_items = list(PortfolioItem.objects.all())

    fallback_images = [
        "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1571330735066-03aaa9429d89?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1551818255-e6e1095bc5c7?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?auto=format&fit=crop&w=900&q=80",
    ]
    specs = [
        {"rot": -8, "depth": 14, "size": "tall", "label": "Live concerts"},
        {"rot": -4, "depth": 10, "size": "short", "label": "Event audio"},
        {"rot": 2, "depth": 8, "size": "tall", "label": "Recording"},
        {"rot": 5, "depth": 12, "size": "short", "label": "Streaming"},
        {"rot": -1, "depth": 6, "size": "med", "label": "Custom builds"},
        {"rot": 3, "depth": 11, "size": "tall", "label": "DJ & nights"},
        {"rot": 6, "depth": 9, "size": "short", "label": "Live sound"},
        {"rot": -3, "depth": 13, "size": "med", "label": "Studio setups"},
    ]
    images = [i.image_url for i in portfolio_items if i.image_url] or []

    hero_cards = []
    for idx in range(8):
        spec = specs[idx]
        hero_cards.append({
            'index': idx + 1,
            'image': images[idx % len(images)] if images else fallback_images[idx],
            'rot': spec['rot'],
            'depth': spec['depth'],
            'size': spec['size'],
            'label': spec['label'],
        })

    context = {
        'portfolio_items': portfolio_items,
        'hero_cards': hero_cards,
        'project_count': len(portfolio_items),
        'service_count': Service.objects.count(),
    }
    return render(request, 'main_app/portfolio.html', context)


def booking(request):
    initial = None
    service_slug = request.GET.get('service')
    if service_slug:
        service = Service.objects.filter(slug=service_slug).first()
        if service:
            initial = {'service': service.pk}

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('HX-Request'):
                return render(request, 'main_app/components/booking_success.html')
            return render(request, 'main_app/booking.html', {'form': BookingForm(), 'service_options': Service.objects.all(), 'submitted': True})
    else:
        form = BookingForm(initial=initial)

    context = {
        'form': form,
        'service_options': Service.objects.all(),
    }
    return render(request, 'main_app/booking.html', context)


def service_price(request, slug):
    service = get_object_or_404(Service, slug=slug)
    return render(request, 'main_app/components/service_price.html', {'service': service})


def pricing(request):
    context = {
        'services': Service.objects.all(),
    }
    return render(request, 'main_app/pricing.html', context)


def learning(request):
    context = {
        'learning_offerings': LearningOffering.objects.all(),
        'categories': LearningOffering.CATEGORY_CHOICES,
        'workshops': Workshop.objects.all(),
        'instructors': TeamMember.objects.filter(is_instructor=True),
        'learning_testimonials': Testimonial.objects.filter(category='learning'),
    }
    return render(request, 'main_app/learning.html', context)


def filter_offerings(request, category):
    if category == 'all':
        offerings = LearningOffering.objects.all()
    else:
        offerings = LearningOffering.objects.filter(category=category)
    return render(request, 'main_app/components/offering_cards.html', {'learning_offerings': offerings})


def hire_the_band(request):
    """Dedicated page for the 'Hire the band' action card (red accent)."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'main_app/hire_the_band.html', {'form': ContactForm(), 'submitted': True})
    else:
        form = ContactForm()
    return render(request, 'main_app/hire_the_band.html', {'form': form, 'submitted': False})


def book_studio(request):
    """Dedicated page for the 'Book studio time' action card (amber accent)."""
    initial = None
    service = Service.objects.filter(slug='audio-setups').first()
    if service:
        initial = {'service': service.pk}
    form = BookingForm(initial=initial)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'main_app/book_studio.html', {
                'form': BookingForm(initial=initial), 'service_options': Service.objects.all(), 'submitted': True,
            })
    return render(request, 'main_app/book_studio.html', {
        'form': form, 'service_options': Service.objects.all(), 'submitted': False,
    })


def what_you_need(request):
    """Dedicated page for the 'Tell us what you need' action card (sky accent)."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'main_app/what_you_need.html', {'form': ContactForm(), 'submitted': True})
    else:
        form = ContactForm()
    return render(request, 'main_app/what_you_need.html', {'form': form, 'submitted': False})


def book_a_lesson(request):
    """Dedicated page for the 'Book a lesson' action card (violet accent)."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'main_app/book_a_lesson.html', {'form': ContactForm(), 'submitted': True})
    else:
        form = ContactForm()
    return render(request, 'main_app/book_a_lesson.html', {'form': form, 'submitted': False})


def register_workshop(request, workshop_id):
    workshop = get_object_or_404(Workshop, id=workshop_id)
    if request.method == 'POST':
        WorkshopRegistration.objects.create(
            workshop=workshop,
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
        )
        return render(request, 'main_app/components/workshop_success.html', {'workshop': workshop})
    return render(request, 'main_app/components/workshop_form.html', {'workshop': workshop})


def about(request):
    context = {
        'team_members': TeamMember.objects.filter(is_instructor=False),
        'about_testimonials': Testimonial.objects.filter(category='about'),
        'portfolio_items': PortfolioItem.objects.filter(is_featured=True)[:6],
    }
    return render(request, 'main_app/about.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('HX-Request'):
                return render(request, 'main_app/components/contact_success.html')
            return render(request, 'main_app/contact.html', {'form': ContactForm(), 'contact_faqs': FAQ.objects.filter(category='contact'), 'submitted': True})
    else:
        form = ContactForm()

    context = {
        'form': form,
        'contact_faqs': FAQ.objects.filter(category='contact'),
    }
    return render(request, 'main_app/contact.html', context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data['email'],
                email=data['email'],
                first_name=data['full_name'],
                password=data['password'],
            )
            UserProfile.objects.create(user=user, intent=data['intent'], intent_detail=data.get('intent_detail', '') or '')
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect(intent_landing(data['intent']))
    else:
        form = RegisterForm()

    return render(request, 'main_app/register.html', {'form': form})


def intent_landing(intent):
    return {
        'learning': 'learning',
        'studio': 'booking',
        'event': 'booking',
        'other': 'home',
    }.get(intent, 'home')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next')
            return redirect(next_url or 'home')
        error = 'Invalid username or password.'

    return render(request, 'main_app/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('home')


def forgot_password(request):
    """Request a password reset link sent to the given email.

    Looks the same to every submitter (no account enumeration): redirects
    to the 'done' page with a neutral message. In DEBUG the reset link is
    also passed to the template so the flow can be tested without an SMTP
    server.
    """
    form = PasswordResetRequestForm()
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].strip().lower()
            user = User.objects.filter(email=email).first()
            if user is not None:
                token = PasswordResetTokenGenerator().make_token(user)
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                path = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
                reset_link = request.build_absolute_uri(path)
                send_mail(
                    'JustTech password reset',
                    f'Click the link below to choose a new password:\n\n{reset_link}\n\n'
                    'If you did not request this, you can ignore this email.\n\n- The JustTech team',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )
                if settings.DEBUG:
                    request.session['reset_link'] = reset_link
            return redirect('password_reset_done')

    return render(request, 'main_app/password_reset.html', {'form': form})


def password_reset_done(request):
    reset_link = request.session.pop('reset_link', None) if settings.DEBUG else None
    return render(request, 'main_app/password_reset_done.html', {'reset_link': reset_link})


def password_reset_confirm(request, uidb64, token):
    """Validate the reset link and let the user set a new password."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not PasswordResetTokenGenerator().check_token(user, token):
        return render(request, 'main_app/password_reset_invalid.html')

    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('password_reset_complete')
    else:
        form = SetNewPasswordForm()

    return render(request, 'main_app/password_reset_confirm.html', {'form': form, 'validlink': True})


def password_reset_complete(request):
    return render(request, 'main_app/password_reset_complete.html')


def debug_static(request):
    """Debug view to check static files configuration.

    Registered only when DEBUG is True (see main_app/urls.py) so it is never
    reachable in production.
    """
    context = {
        'debug': settings.DEBUG,
        'static_url': settings.STATIC_URL,
        'static_dirs': settings.STATICFILES_DIRS,
        'static_root': settings.STATIC_ROOT,
    }
    return render(request, 'main_app/debug_static.html', context)


def robots_txt(request):
    """Simple robots.txt. Domain-aware so it works in any environment."""
    host = request.get_host()
    robot_txt = f"""User-agent: *
Allow: /
Disallow: /admin/
Disallow: /login/

Sitemap: https://{host}/sitemap.xml
"""
    return HttpResponse(robot_txt, content_type='text/plain')
