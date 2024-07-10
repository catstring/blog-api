from django.urls import path
from .views import PostListCreate, PostDetail, TagList, increment_view_count

urlpatterns = [
    path('posts/', PostListCreate.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('posts/<int:pk>/view/', increment_view_count, name='increment-view-count'),
    path('tags/', TagList.as_view(), name='tag-list'),  
]
