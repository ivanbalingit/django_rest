"""django_rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api import views

user_signup    = views.UserViewSet.as_view({'post': 'create'})
post_list      = views.PostViewSet.as_view({'get': 'list', 'post': 'create'})
post_detail    = views.PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
user_posts     = views.PostViewSet.as_view({'get': 'user_posts'})
post_comments  = views.CommentViewSet.as_view({'get': 'list', 'post': 'create'})
comment_detail = views.CommentViewSet.as_view({'delete': 'destroy'})

urlpatterns = [
    path('auth/signup/', user_signup, name="user-create"),                                        # Feature 1
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),                 # Feature 2
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('posts/', post_list, name="post-list"),                                                  # Feature 3, 7
    path('posts/<int:pk>/', post_detail, name='post-detail'),                                     # Feature 4, 5, 8
    path('me/posts/', user_posts, name="user-posts"),                                             # Feature 6

    path('posts/<int:post_id>/comments/', post_comments, name="comment-list"),                    # Feature 9, 11
    path('posts/<int:post_id>/comments/<int:comment_id>', comment_detail, name="comment-detail"), # Feature 10

    path('admin/', admin.site.urls),
]
