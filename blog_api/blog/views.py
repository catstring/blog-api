from rest_framework import generics, permissions, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes
from .models import Post, Tag
from .serializers import PostSerializer, PostCreateUpdateSerializer, TagSerializer
import logging
import json

logger = logging.getLogger(__name__)

class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    filter_backends = [SearchFilter]
    search_fields = ['title', 'content']
    permission_classes = [IsAuthenticatedOrReadOnly]

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

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(title__icontains=search_query) | queryset.filter(content__icontains=search_query)
        return queryset

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            self.authentication_classes = [JWTAuthentication]
            return PostCreateUpdateSerializer
        return PostSerializer

class TagList(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def update_like_count(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        post.like_count = request.data.get('like_count', post.like_count)
        post.save()
        return Response({'status': 'success', 'like_count': post.like_count}, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response({'status': 'error', 'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error updating like count: {e}")
        return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def increment_view_count(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        post.view_count += 1
        post.save()
        return Response({'status': 'success', 'view_count': post.view_count}, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response({'status': 'error', 'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error updating view count: {e}")
        return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)