from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.exceptions import TokenBackendError

from django.contrib.auth.models import User
from api.models import Post, Comment
from api.serializers import CommentSerializer, PostSerializer, UserSerializer

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

    def create(self, request):
        user = User.objects.create(username=request.data['username'], email=request.data['email'])
        user.set_password(request.data['password'])
        user.save()

        if user:
            serializer = UserSerializer(user, context={'request': request})
            return Response({'message': "Signup successful!", 'data': serializer.data})
        else:
            return Response({'message': "Signup unsuccessful."})

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

    def destroy(self, request, pk):
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

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes_by_action = {'create':     [permissions.IsAuthenticated],
                                    'update':     [permissions.IsAuthenticated],
                                    'destroy':    [permissions.IsAuthenticated],
                                    'list':       [permissions.AllowAny]}

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        queryset = Comment.objects.filter(post__id=post_id)
        return queryset

    def create(self, request, post_id):
        user = get_user_from_token(request)
        
        try: 
            post    = Post.objects.get(id=post_id)
            comment = Comment.objects.create(user=user, post=post, content=request.data['content'])

            msg = "Comment created!"
            serializer = CommentSerializer(comment, context={'request': request})
            return Response({'message': msg, 'data': serializer.data})           
        except Post.DoesNotExist:
            msg = "Comment create unsuccessful."
            return Response({'message': msg})

    def destroy(self, request, post_id, comment_id):
        user = get_user_from_token(request)
        
        try:
            post    = Post.objects.get(id=post_id)
            comment = Comment.objects.get(id=comment_id)
 
            if user == post.user or user == comment.user:
                comment.delete()
                msg = "Comment deleted!"            
        except (Post.DoesNotExist, Comment.DoesNotExist):
            msg = "Comment delete unsuccessful."

        return Response({'message': msg})
