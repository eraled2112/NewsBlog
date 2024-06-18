from django.urls import path, include
from .views import (
    NewsListApiView,
    NewsDetailApiView
)

urlpatterns = [
    path('api/', NewsListApiView.as_view()),
    path('api/<int:news_id>/', NewsDetailApiView.as_view()),
]
