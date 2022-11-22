from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('list/', views.PostList.as_view(), name='list'),
    path('upload/', views.Upload.as_view(), name='upload'),
    path('delete/', views.Delete.as_view(), name='delete'),
    path('reply/upload/<str:pk>/', views.ReplyUpload.as_view(), name='upload_reply'),
    path('reply/delete/', views.ReplyDelete.as_view(), name='delete_reply'),
    path('reply/list/', views.GetReply.as_view(), name='reply_list'),
    path('reply/list/<str:pk>/', views.GetRepList.as_view(), name='reply_list_of_post'),
    path('like/', views.Liked.as_view(), name='like'),
    path('repost/', views.Reposted.as_view(), name='repost'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)