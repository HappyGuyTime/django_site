from django.urls import path

from .views import HiBlogView, ArticlesListView, ArticleDetailView, LatestArticleFeed


app_name = 'blogapp'

urlpatterns = [
    path('hello/', HiBlogView.as_view(), name='hello'),
    path('articles/', ArticlesListView.as_view(), name='articles'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article'),
    path('articles/latest/feed/', LatestArticleFeed(), name='articles_feed'),
]
