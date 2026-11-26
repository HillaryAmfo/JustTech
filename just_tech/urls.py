from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
]

# Serve static and media files only during development. In production the
# hosting platform must serve /static/ (after collectstatic) and /media/.
static_dirs = getattr(settings, 'STATICFILES_DIRS', ())
if static_dirs:
    static_root = (
        str(static_dirs[0])
        if settings.DEBUG
        else str(settings.STATIC_ROOT)
    )
    urlpatterns = [
        re_path(
            r'^static/(?P<path>.*)$',
            serve,
            {'document_root': static_root},
        ),
        *urlpatterns,
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)