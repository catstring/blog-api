# blog/urls.py

from django.urls import path
from .views import PostListCreate, PostDetail, TagListCreate, UserDetail

urlpatterns = [
    path('posts/', PostListCreate.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('tags/', TagListCreate.as_view(), name='tag-list-create'),
    path('user/', UserDetail.as_view(), name='user-detail'),
]
