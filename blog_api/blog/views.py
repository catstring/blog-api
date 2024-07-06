# blog/views.py

from rest_framework import generics, permissions
from .models import Post, Tag
from .serializers import PostSerializer, PostCreateUpdateSerializer, TagSerializer, UserSerializer
from rest_framework.filters import SearchFilter
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['tags__name']
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateUpdateSerializer
        return PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PostCreateUpdateSerializer
        return PostSerializer

class TagListCreate(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user