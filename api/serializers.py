from rest_framework import serializers

from django.contrib.auth.models import User
from api.models import Post, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source='user.username')

    class Meta:
        model = Post
        fields = ['id', 'username', 'created', 'title', 'content']

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source='user.username')
    post_id = serializers.IntegerField(read_only=True, source='post.id')

    class Meta:
        model = Comment
        fields = ['id', 'post_id', 'username', 'created', 'content']
