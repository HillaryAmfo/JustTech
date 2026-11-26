from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from . import views
from .sitemaps import StaticViewSitemap

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('booking/', views.booking, name='booking'),
    path('booking/service-price/<slug:slug>/', views.service_price, name='service_price'),
    path('pricing/', views.pricing, name='pricing'),
    path('learning/', views.learning, name='learning'),
    path('learning/filter/<str:category>/', views.filter_offerings, name='filter_offerings'),
    path('learning/register-workshop/<int:workshop_id>/', views.register_workshop, name='register_workshop'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms/', views.terms, name='terms'),
    path('hire-the-band/', views.hire_the_band, name='hire_the_band'),
    path('book-studio/', views.book_studio, name='book_studio'),
    path('what-you-need/', views.what_you_need, name='what_you_need'),
    path('book-a-lesson/', views.book_a_lesson, name='book_a_lesson'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('forgot-password/<str:uidb64>/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('forgot-password/done/', views.password_reset_done, name='password_reset_done'),
    path('forgot-password/complete/', views.password_reset_complete, name='password_reset_complete'),
    path('logout/', views.logout_view, name='logout'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': {'static': StaticViewSitemap()}}, name='django.contrib.sitemaps.views.sitemap'),
]

# Dev-only diagnostics. Never registered in production.
if settings.DEBUG:
    urlpatterns.append(path('debug-static/', views.debug_static, name='debug_static'))