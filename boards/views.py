from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from boards.models import Board
from boards.serializers import BoardDetailSerializer, BoardListSerializer, BoardCreateSerializer
from rest_framework.generics import get_object_or_404


class BoardListView(APIView):
    def get(self, request, boardtype):
        boards = Board.objects.filter(boardtype=boardtype)
        serializer = BoardListSerializer(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, boardtype):
        serializer = BoardCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=10)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class BoardDetailView(APIView):
    def get(self, request, boardtype, board_id):
        boards = get_object_or_404(Board, id=board_id)
        serializer = BoardDetailSerializer(boards)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, boardtype, board_id):
        pass
    
    def delete(self, request, boardtype, board_id):
        pass