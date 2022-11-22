from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('profile_update/', views.ProfileUpdate.as_view(), name='profile_update'),
    path('profile_delete/', views.ProfileDelete.as_view(), name='profile_delete'),
    path('profile/<str:pk>/', views.GetProfile.as_view(), name='get_profile'),
    path('follow/', views.Follow.as_view(), name='follow'),
    path('suggestions/', views.Suggest.as_view(), name='suggestions'),
    path('search/<str:uk>/<str:pk>/', views.Search.as_view(), name='search'),
    path('get-user/', views.GetUser.as_view(), name='get-user')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
