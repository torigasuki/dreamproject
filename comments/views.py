from rest_framework import status , permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CommentSerializer,CommentCreateSerializer,ReCommentSerializer,ReCommentCreateSerializer

# Create your views here.
class Comment(APIView):
    def get(self, request, board_id):
        boards = get_object_or_404(Board, id=board_id)
        comments = boards.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, board_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, board_id=board_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self,request,board_id,comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        serializer = CommentCreateSerializer(comment,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self,request,board_id,comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        return Response(status=status.HTTP_200_OK)


class ReComment(APIView):
    def get(self, request, comment_id):
        comments = get_object_or_404(Comment, id=comment_id)
        recomments = comments.recomments.all()
        serializer = ReCommentSerializer(recomments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, comment_id):
        serializer = ReCommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, comment_id=comment_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self,request,comment_id,recomment_id):
        recomment = get_object_or_404(ReComment, id=recomment_id)
        serializer = ReCommentCreateSerializer(recomment,data=request.data)
        if serializer.is_valid():
            serializer.save(recomment_id=recomment_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self,request,comment_id,recomment_id):
        comment = get_object_or_404(Comment, id=recomment_id)
        comment.delete()
        return Response(status=status.HTTP_200_OK)
    
    