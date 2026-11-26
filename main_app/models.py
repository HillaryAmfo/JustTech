from django.conf import settings
from django.db import models


class SiteSettings(models.Model):
    company_name = models.CharField(max_length=120, default='Just Tech')
    tagline = models.CharField(max_length=255, default='Professional Audio & Visual Services')
    primary_email = models.EmailField(default='info@justtech.com')
    booking_email = models.EmailField(default='bookings@justtech.com')
    phone = models.CharField(max_length=50, default='+1 (555) 123-4567')
    address_line_1 = models.CharField(max_length=255, default='123 Tech Avenue, Suite 400')
    address_line_2 = models.CharField(max_length=255, blank=True, default='San Francisco, CA 94107')
    business_hours = models.TextField(default='Monday - Friday: 9:00 AM - 6:00 PM\nSaturday: 10:00 AM - 4:00 PM\nSunday: Closed')
    service_area = models.CharField(max_length=255, default='San Francisco Bay Area')

    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)

    privacy_policy_url = models.URLField(blank=True)
    terms_url = models.URLField(blank=True)

    projects_completed_text = models.CharField(max_length=50, default='500+')
    client_satisfaction_text = models.CharField(max_length=50, default='98%')
    students_trained_text = models.CharField(max_length=50, default='250+')
    support_availability_text = models.CharField(max_length=50, default='24/7')

    founded_year = models.PositiveSmallIntegerField(default=2018)

    def __str__(self):
        return 'Site Settings'


class Service(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    icon_class = models.CharField(max_length=100, default='fas fa-tools')
    short_description = models.TextField()
    feature_1 = models.CharField(max_length=255, blank=True)
    feature_2 = models.CharField(max_length=255, blank=True)
    feature_3 = models.CharField(max_length=255, blank=True)
    starting_price = models.CharField(max_length=60, blank=True, help_text='Ex: Starting at $299')
    is_featured = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class PortfolioItem(models.Model):
    title = models.CharField(max_length=120)
    image_url = models.URLField()
    category = models.CharField(max_length=120, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['display_order', 'title']

    def __str__(self):
        return self.title


class PricingPackage(models.Model):
    name = models.CharField(max_length=120)
    price = models.CharField(max_length=60)
    description = models.TextField()
    feature_1 = models.CharField(max_length=255, blank=True)
    feature_2 = models.CharField(max_length=255, blank=True)
    feature_3 = models.CharField(max_length=255, blank=True)
    feature_4 = models.CharField(max_length=255, blank=True)
    feature_5 = models.CharField(max_length=255, blank=True)
    feature_6 = models.CharField(max_length=255, blank=True)
    is_popular = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class EquipmentItem(models.Model):
    name = models.CharField(max_length=120)
    icon_class = models.CharField(max_length=100, default='fas fa-microphone')
    price = models.CharField(max_length=60)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('contact', 'Contact'),
        ('pricing', 'Pricing'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'question']

    def __str__(self):
        return f'{self.get_category_display()}: {self.question}'


class TeamMember(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    bio = models.CharField(max_length=255)
    image_url = models.URLField(blank=True)
    is_instructor = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    CATEGORY_CHOICES = [
        ('about', 'About'),
        ('learning', 'Learning'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    quote = models.TextField()
    author_name = models.CharField(max_length=120)
    author_title = models.CharField(max_length=120, blank=True)
    image_url = models.URLField(blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'author_name']

    def __str__(self):
        return f'{self.author_name} ({self.get_category_display()})'


class LearningOffering(models.Model):
    CATEGORY_CHOICES = [
        ('audio', 'Audio Production'),
        ('visual', 'Visual Design'),
        ('instrument', 'Instrument'),
        ('production', 'Music Production'),
        ('tech', 'Technical Skills'),
    ]

    SKILL_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('all-levels', 'All Levels'),
    ]

    title = models.CharField(max_length=120)
    icon_class = models.CharField(max_length=100, default='fas fa-graduation-cap')
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='audio')
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES, default='all-levels')
    curriculum = models.TextField(blank=True, help_text='One topic per line')
    duration = models.CharField(max_length=100, blank=True)
    feature_1 = models.CharField(max_length=255, blank=True)
    feature_2 = models.CharField(max_length=255, blank=True)
    feature_3 = models.CharField(max_length=255, blank=True)
    starting_price = models.CharField(max_length=60, blank=True)
    cta_label = models.CharField(max_length=60, default='Enroll Now')
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'title']

    def __str__(self):
        return self.title


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    TIME_CHOICES = [
        ('morning', 'Morning (9AM - 12PM)'),
        ('afternoon', 'Afternoon (12PM - 5PM)'),
        ('evening', 'Evening (5PM - 8PM)'),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    company = models.CharField(max_length=120, blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    preferred_date = models.DateField(null=True, blank=True)
    preferred_time = models.CharField(max_length=20, choices=TIME_CHOICES, default='morning')
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.service.name if self.service else "Inquiry"} ({self.get_status_display()})'


class Workshop(models.Model):
    title = models.CharField(max_length=120)
    date_label = models.CharField(max_length=60)
    duration_label = models.CharField(max_length=40)
    price_label = models.CharField(max_length=40)
    availability_label = models.CharField(max_length=60)
    availability_class = models.CharField(max_length=40, default='text-red-500')
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'title']

    def __str__(self):
        return self.title


class WorkshopRegistration(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='registrations')
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.workshop.title}'


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=160)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.subject}'


class UserProfile(models.Model):
    INTENT_CHOICES = [
        ('learning', 'Learning'),
        ('studio', 'Book a studio session'),
        ('event', 'Events & production'),
        ('other', 'Something else'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    intent = models.CharField(max_length=20, choices=INTENT_CHOICES, default='other')
    intent_detail = models.CharField(max_length=255, blank=True, help_text='Contextual answer for the selected intent (e.g. what to learn, session type).')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.get_username()} - {self.get_intent_display()}'
