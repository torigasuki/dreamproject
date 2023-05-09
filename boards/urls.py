from django.urls import path
from boards import views

urlpatterns = [
    path('<str:boardtype>/', views.BoardListView.as_view(), name='board_list_view'),
    path('<str:boardtype>/<int:board_id>/', views.BoardDetailView.as_view(), name='board_detail_view')
]
