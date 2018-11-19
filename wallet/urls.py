""" Default urlconf for wallet """

from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('base.urls')),
]

if settings.DEBUG:
    # Add debug-toolbar
    import debug_toolbar  # noqa
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))

    # Serve media files through Django.
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
