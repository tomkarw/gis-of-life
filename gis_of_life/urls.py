from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from gis_of_life import settings
from gis_of_life.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name="homepage"),
    path('accounts/', include('accounts.urls')),
    path('game/', include('game.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
