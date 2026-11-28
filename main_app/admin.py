from django.contrib import admin

from .models import (
    Booking,
    ContactMessage,
    EquipmentItem,
    FAQ,
    LearningOffering,
    PortfolioItem,
    PricingPackage,
    Service,
    SiteSettings,
    TeamMember,
    Testimonial,
    UserProfile,
    Workshop,
    WorkshopRegistration,
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'primary_email', 'phone')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'starting_price', 'is_featured', 'is_popular', 'display_order')
    list_filter = ('is_featured', 'is_popular')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'display_order')
    list_filter = ('is_featured',)


@admin.register(PricingPackage)
class PricingPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_popular', 'display_order')
    list_filter = ('is_popular',)


@admin.register(EquipmentItem)
class EquipmentItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'display_order')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'display_order')
    list_filter = ('category',)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'specialisation', 'is_instructor', 'display_order')
    list_filter = ('is_instructor',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'category', 'display_order')
    list_filter = ('category',)


@admin.register(LearningOffering)
class LearningOfferingAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'skill_level', 'starting_price', 'is_featured', 'display_order')
    list_filter = ('category', 'skill_level', 'is_featured')


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_label', 'price_label', 'display_order')


@admin.register(WorkshopRegistration)
class WorkshopRegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'workshop', 'email', 'created_at')
    list_filter = ('workshop',)
    search_fields = ('name', 'email')
    date_hierarchy = 'created_at'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'preferred_date', 'preferred_time', 'status', 'created_at')
    list_filter = ('status', 'service', 'preferred_date')
    search_fields = ('name', 'email', 'phone')
    date_hierarchy = 'created_at'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'intent', 'created_at')
    list_filter = ('intent',)
    search_fields = ('user__username', 'user__email')
    date_hierarchy = 'created_at'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    date_hierarchy = 'created_at'
