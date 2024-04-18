from django.contrib import admin
from django.urls import path, include

# To show media files
from django.conf import settings
from django.contrib.staticfiles.urls import static

from django.conf.urls import handler404
from shop.views import error_404_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('account/', include('accounts.urls')),
    path('shop/', include('order.urls')),
    path('payment/', include('payment.urls')),
    path('', include('newsletter.urls')),
]

if settings.DEBUG == True or settings.DEBUG == False:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = error_404_view
