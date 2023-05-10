from django.urls import path, include
from boards import views

urlpatterns = [
    path('', views.BoardListView.as_view(), name='board_list_view'),
    path('<str:boardtype>/', views.BoardListView.as_view(), name='board_list_view'),
    path('<str:boardtype>/<int:board_id>/', views.BoardDetailView.as_view(), name='board_detail_view'),
    path('<str:boardtype>/<int:board_id>/comments/',include("comments.urls")),
]
