from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from boards.serializers import BoardDetailSerializer, BoardListSerializer, BoardCreateSerializer
from boards.models import Board
from django.db.models import Max


class BoardListView(APIView):
    def get(self, request, boardtype=None):
        if boardtype:
            boards = Board.objects.filter(boardtype=boardtype).order_by('-created_at')
            serializer = BoardListSerializer(boards, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            boardtype_list=['BOARDTOSLEEP','BOARDTOAWAKE','BOARDTOHEAL']
            data = []
            for boardtype in boardtype_list:
                boards = Board.objects.filter(boardtype=boardtype).annotate(latest_date=Max('created_at')).order_by('-latest_date')[:5]
                serializer = BoardListSerializer(boards, many=True)
                data+=serializer.data
            return Response(data, status=status.HTTP_200_OK)
        

    def post(self, request):
        serializer = BoardCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardDetailView(APIView):
    def get(self, request, boardtype, board_id):
        boards = get_object_or_404(Board, id=board_id) 
        serializer = BoardDetailSerializer(boards)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, boardtype, board_id):
        board = get_object_or_404(Board, id=board_id)
        if request.user == board.user:
            serializer = BoardCreateSerializer(board, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("수정 권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, boardtype, board_id):
        board = get_object_or_404(Board, id=board_id)
        if request.user == board.user:
            board.delete()
            return Response("삭제되었습니다.", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("삭제 권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

class LikeView(APIView):
    def post(self, request, boardtype, board_id):
        board = get_object_or_404(Board, id=board_id)
        if request.user in board.likes.all():
            board.likes.remove(request.user)
            return Response("좋아요 취소했습니다.", status=status.HTTP_200_OK)
        else:
            board.likes.add(request.user)
            return Response("좋아요 했습니다.", status=status.HTTP_200_OK)


# class BookMarkView(APIView):
#     def get(self, request, board_id):
#         return Response()
#     def post(self, request,board_id):
#         board = get_object_or_404(Board, id=board_id)
#         if request.user in board.bookmarks.all():
#             board.bookmarks.remove(request.user)
#             return Response("북마크 취소했습니다.", status=status.HTTP_200_OK)
#         else:
#             board.bookmarks.add(request.user)
#             return Response("북마크 했습니다.", status=status.HTTP_200_OK)