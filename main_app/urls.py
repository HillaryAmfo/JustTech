from django.urls import path
from . import views

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
    path('debug-static/', views.debug_static, name='debug_static'),  # Add this
]