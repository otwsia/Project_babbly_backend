from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app_profiles.urls')),
    path('jwt-api/', include('authentication_w_jwt.urls')),
    path('post/', include('app_posts.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
