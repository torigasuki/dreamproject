from django.contrib import admin
from django.urls import path
from comments import views

urlpatterns = [
    path('', views.CommentView.as_view(), name='comment'),
    path('<int:comment_id>/', views.CommentView.as_view(), name='comment_ud'),
    path('<int:comment_id>/re/', views.ReCommentView.as_view(), name='re_comment'),
    path('<int:comment_id>/re/<int:recomment_id>', views.ReCommentView.as_view(), name='re_comment_ud')
]
