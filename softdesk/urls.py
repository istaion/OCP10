"""softdesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from authentication.views import UserSignupView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from projects.views import (
    ProjectsView,
    ProjectIdView,
    ContributorsView,
    IssuesView,
    CommentView,
    CommentIdView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('signup/', UserSignupView.as_view({'post': 'create'}), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('projects/', ProjectsView.as_view({'get': 'list', 'post': 'create'})),
    path('projects/<int:project_id>/', ProjectIdView.as_view({'get': 'retrieve', 'put': 'update',
                                                              'delete': 'delete'})),
    path('projects/<int:project_id>/users/', ContributorsView.as_view({'get': 'list', 'post': 'create'})),
    path('projects/<int:project_id>/users/<int:user_id>/', ContributorsView.as_view({'delete': 'delete'})),
    path('projects/<int:project_id>/issues/', IssuesView.as_view({'get': 'list', 'post': 'create'})),
    path('projects/<int:project_id>/issues/<int:issue_id>/', IssuesView.as_view({'put': 'update',
                                                              'delete': 'delete'})),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/', CommentView.as_view({'get': 'list',
                                                                                           'post': 'create'})),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>/',
         CommentIdView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'delete'})),
]
