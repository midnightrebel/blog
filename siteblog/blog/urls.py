from django.contrib.auth.decorators import login_required
from django.urls import path, re_path

from . import views
from .models import *
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('category/<str:slug>/', PostsByCategory.as_view(), name='category'),
    path('post/<str:slug>/', GetPost.as_view(), name='post'),
    path('tag/<str:slug>/', PostsByTags.as_view(), name='tag'),
    path('search/', Search.as_view(), name='search'),
    re_path(r'^article/(?P<pk>d+)/like/$',
            login_required(views.VotesView.as_view(model=Post, vote_type=LikeDislike.LIKE)),
            name='article'),
    re_path(r'^comment/(?P<pk>d+)/like/$',
            login_required(views.VotesView.as_view(model=Comment, vote_type=LikeDislike.LIKE)),
            name='comment')

]
