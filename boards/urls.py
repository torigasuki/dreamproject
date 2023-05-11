from django.urls import path, include
from boards import views

urlpatterns = [
    path('', views.BoardListView.as_view(), name='board_list_view'),
    path('<str:boardtype>/', views.BoardListView.as_view(), name='board_list_view'),
    path('<str:boardtype>/<int:board_id>/', views.BoardDetailView.as_view(), name='board_detail_view'),
    path('<str:boardtype>/<int:board_id>/comments/',include("comments.urls")),
    path('<str:boardtype>/<int:board_id>/like/', views.LikeView.as_view(), name='like_view'),
   #path('<str:boardtype>/<int:board_id>/bookmark/', views.BookMarkView.as_view(), name='bookmark_view'),
]
