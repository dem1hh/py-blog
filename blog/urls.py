from django.contrib import admin
from django.urls import path, include

import blog
from blog.views import index, PostDetailView

app_name = 'blog'

urlpatterns = [
    path("", index, name="index"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
]
