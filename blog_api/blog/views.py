from rest_framework import generics, permissions, status
from .models import Post
from .serializers import PostSerializer, PostCreateUpdateSerializer
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging

logger = logging.getLogger(__name__)

class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    filter_backends = [SearchFilter]
    search_fields = ['title', 'content']
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow read-only access for unauthenticated users

    def get_serializer_class(self):
        if self.request.method == 'POST':
            self.authentication_classes = [JWTAuthentication]
            return PostCreateUpdateSerializer
        return PostSerializer

    def perform_create(self, serializer):
        try:
            post = serializer.save()
            response_serializer = PostSerializer(post)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating post: {e}")
            return Response({"error": "Error creating post"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            self.authentication_classes = [JWTAuthentication]
            return PostCreateUpdateSerializer
        return PostSerializer
