from django.contrib import admin
from django.urls import path
from comments import views

urlpatterns = [
    path('', views.Comment.as_view(), name='comment'),
    path('<int:comment_id>/', views.Comment.as_view(), name='comment_ud'),
    path('<int:comment_id>/re/', views.ReComment.as_view(), name='re_comment'),
    path('<int:comment_id>/re/<int:recomment_id>', views.ReComment.as_view(), name='re_comment_ud')
]
