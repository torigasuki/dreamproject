from rest_framework import serializers

from boards.models import Board

class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ("pk", "title", "updated_at", "boardtype", "image","likes")
        

class BoardDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

class BoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ("title", "content", "image", "boardtype")