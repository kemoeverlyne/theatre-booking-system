"""theatre_booking_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.http import HttpResponse


schema_view = get_schema_view(
   openapi.Info(
      title="Theatre Booking API",
      default_version='v1',
      description="API for theatre booking system",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@theatre.local"),
      license=openapi.License(name="License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

if not settings.TESTING and not settings.DEBUG:
    handler404 = "theatre_booking_system.views.error_404"
    handler500 = "theatre_booking_system.views.error_500"
    handler403 = "theatre_booking_system.views.error_403"
    handler400 = "theatre_booking_system.views.error_400"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('booking.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Django Debug Toolbar only in DEBUG mode
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

# Additional endpoints for testing/debugging
if settings.TESTING or settings.DEBUG:
    from cacheops import invalidate_all
    
    def trigger_error(request):
        # Test Sentry
        division_by_zero = 1 / 0
        return division_by_zero
    
    def invalidate_cache(request):
        # Invalidate Cache
        invalidate_all()
        return HttpResponse("Cache invalidated")
    
    urlpatterns += [
        path("sentry-debug/", trigger_error),
        path("invalidate-cache/", invalidate_cache),
    ]
