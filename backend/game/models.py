from django.db import models


class GameSession(models.Model):
    """游戏会话模型"""
    board = models.JSONField(default=list)  # 4x4游戏板
    score = models.IntegerField(default=0)  # 当前分数
    best_score = models.IntegerField(default=0)  # 最高分
    game_over = models.BooleanField(default=False)  # 游戏是否结束
    won = models.BooleanField(default=False)  # 是否获胜
    previous_board = models.JSONField(default=list, null=True)  # 上一步的棋盘状态
    previous_score = models.IntegerField(default=0, null=True)  # 上一步的分数
    has_undone = models.BooleanField(default=False)  # 是否已撤销（每局只允许撤销一次）
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
