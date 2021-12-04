from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.exceptions import TokenBackendError

from django.contrib.auth.models import User
from api.models import Post
from api.serializers import PostSerializer, UserSerializer

def get_user_from_token(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        token_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
        user = User.objects.get(id=token_data['user_id'])
        return user
    except TokenBackendError:
        print("Token expired.")
        return None

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes_by_action = {'create':     [permissions.IsAuthenticated],
                                    'update':     [permissions.IsAuthenticated],
                                    'destroy':    [permissions.IsAuthenticated],
                                    'user_posts': [permissions.IsAuthenticated],
                                    'list':       [permissions.AllowAny]}

    def create(self, request):
        user = get_user_from_token(request)
        post = Post.objects.create(user=user, title=request.data['title'], content=request.data['content'])
        
        if post: msg = "Post created!"
        else:    msg = "Post create unsuccessful."
        
        serializer = PostSerializer(post, context={'request': request})
        return Response({'message': msg, 'data': serializer.data})

    def update(self, request, pk=None):
        user = get_user_from_token(request)

        try: 
            post = Post.objects.get(id=pk, user=user)
            post.title   = request.data['title']
            post.content = request.data['content']
            post.save()

            msg = "Post updated!"
            serializer = PostSerializer(post, context={'request': request})
            return Response({'message': msg, 'data': serializer.data})
        except Post.DoesNotExist:
            msg = "Post update unsuccessful."
            return Response({'message': msg})

    def destroy(self, request, pk=None):
        user = get_user_from_token(request)

        try: 
            post = Post.objects.get(id=pk, user=user)
            post.delete()
            msg = "Post deleted!"            
        except Post.DoesNotExist:
            msg = "Post delete unsuccessful."

        return Response({'message': msg})

    def user_posts(self, request):
        user = get_user_from_token(request)
        posts = Post.objects.filter(user=user)
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response({'message': "Success!", 'data': serializer.data})

    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
