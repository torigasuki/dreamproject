from django.db import models
from boards.models import Board
from users.models import User

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    user = models.ForeignKey(User , on_delete=models.SET_NULL, null=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='comments')    
    
    
class ReComment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    user = models.ForeignKey(User , on_delete=models.SET_NULL, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='recomments')        
    
