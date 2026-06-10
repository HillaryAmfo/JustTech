from django.conf import settings
from django.shortcuts import get_object_or_404, render

from .forms import BookingForm
from .models import (
    EquipmentItem,
    FAQ,
    LearningOffering,
    PortfolioItem,
    PricingPackage,
    Service,
    SiteSettings,
    TeamMember,
    Testimonial,
    Workshop,
    WorkshopRegistration,
)


def home(request):
    context = {
        'featured_services': Service.objects.filter(is_featured=True)[:3],
        'featured_portfolio': PortfolioItem.objects.filter(is_featured=True)[:6],
    }
    return render(request, 'main_app/index.html', context)


def services(request):
    context = {
        'services': Service.objects.all(),
    }
    return render(request, 'main_app/services.html', context)


def portfolio(request):
    context = {
        'portfolio_items': PortfolioItem.objects.all(),
    }
    return render(request, 'main_app/portfolio.html', context)


def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('HX-Request'):
                return render(request, 'main_app/components/booking_success.html')
            return render(request, 'main_app/booking.html', {'form': BookingForm(), 'service_options': Service.objects.all(), 'popular_services': Service.objects.filter(is_popular=True)[:3], 'submitted': True})
    else:
        form = BookingForm()

    context = {
        'form': form,
        'service_options': Service.objects.all(),
        'popular_services': Service.objects.filter(is_popular=True)[:3],
    }
    return render(request, 'main_app/booking.html', context)


def service_price(request, slug):
    service = get_object_or_404(Service, slug=slug)
    return render(request, 'main_app/components/service_price.html', {'service': service})


def pricing(request):
    context = {
        'packages': PricingPackage.objects.all(),
        'equipment_items': EquipmentItem.objects.all(),
        'pricing_faqs': FAQ.objects.filter(category='pricing'),
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
    }
    return render(request, 'main_app/about.html', context)


def contact(request):
    context = {
        'contact_faqs': FAQ.objects.filter(category='contact'),
    }
    return render(request, 'main_app/contact.html', context)


def debug_static(request):
    """Debug view to check static files configuration"""
    context = {
        'debug': settings.DEBUG,
        'static_url': settings.STATIC_URL,
        'static_dirs': settings.STATICFILES_DIRS,
        'static_root': settings.STATIC_ROOT,
    }
    return render(request, 'main_app/debug_static.html', context)
