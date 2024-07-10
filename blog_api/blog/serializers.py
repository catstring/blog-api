from rest_framework import serializers
from .models import Post, Tag

class TagSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField(method_name='get_post_count')

    class Meta:
        model = Tag
        fields = ['id', 'name', 'post_count']

    def get_post_count(self, obj):
        return obj.posts.count()

class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_names = serializers.ListField(
        child=serializers.CharField(max_length=30), write_only=True
    )

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'created_at', 'updated_at', 
            'view_count', 'like_count', 'tags', 'tag_names'
        ]

    def create(self, validated_data):
        tag_names = validated_data.pop('tag_names', [])
        post = Post.objects.create(**validated_data)
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            post.tags.add(tag)
        return post

    def update(self, instance, validated_data):
        tag_names = validated_data.pop('tag_names', [])
        instance = super().update(instance, validated_data)
        if tag_names:
            instance.tags.clear()
            for name in tag_names:
                tag, created = Tag.objects.get_or_create(name=name)
                instance.tags.add(tag)
        return instance

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    tag_names = serializers.ListField(
        child=serializers.CharField(max_length=30), write_only=True
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'view_count', 'like_count', 'tag_names']

    def create(self, validated_data):
        tag_names = validated_data.pop('tag_names', [])
        post = Post.objects.create(**validated_data)
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            post.tags.add(tag)
        return post

    def update(self, instance, validated_data):
        tag_names = validated_data.pop('tag_names', [])
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.view_count = validated_data.get('view_count', instance.view_count)
        instance.like_count = validated_data.get('like_count', instance.like_count)
        instance.save()

        # Clear existing tags and add new ones
        instance.tags.clear()
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            instance.tags.add(tag)

        return instance
