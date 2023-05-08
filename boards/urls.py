from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("boards/<int:board_id>/comments/",include("comments.urls")),
]
