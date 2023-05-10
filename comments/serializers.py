from rest_framework import serializers
from .models import Comment,ReComment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model:Comment
        fields = ['id', 'content', 'created_at', 'user', 'board']
        
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model:Comment
        fields = ['content']
    
    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        return instance.save()
        
class ReCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model:ReComment
        fields = ['id', 'content', 'created_at', 'user', 'comment']
        
class ReCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model:ReComment
        fields = ['content']
        
    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        return instance.save()
        