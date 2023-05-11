from rest_framework import serializers

from boards.models import Board

class BoardListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    def get_user(self,obj):
        return obj.user.nickname
    
    class Meta:
        model = Board
        fields = ("pk", "title", "created_at", "boardtype", "image","likes","user")
        

class BoardDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

class BoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ("title", "content", "image", "boardtype")