from rest_framework import serializers

from django.contrib.auth.models import User
from api.models import Post

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'password']

class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source='user.username')

    class Meta:
        model = Post
        fields = ['id', 'username', 'created', 'title', 'content']
