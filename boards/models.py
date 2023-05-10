from django.db import models
from users.models import User

class Board(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(blank=True, upload_to='%Y/%m/')
    BOARD_TYPE_CHOICES = [
        ('BOARDTOSLEEP', '잘 자는 방법 게시판'),
        ('BOARDTOAWAKE', '안 자는 방법 게시판'),
        ('BOARDTOHEAL', '수면장애 치료 공유방'),
    ]
    boardtype = models.CharField(max_length=20, choices = BOARD_TYPE_CHOICES, error_messages={'message':'게시판 종류는 필수 선택 사항입니다.'})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)