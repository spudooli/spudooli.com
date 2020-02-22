from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostIndex.as_view(), name='home'),
    path('postlist', views.PostList.as_view(), name='postlist'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]