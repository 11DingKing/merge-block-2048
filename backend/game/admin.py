from django.contrib import admin
from .models import GameSession


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'score', 'best_score', 'game_over', 'won', 'created_at']
    list_filter = ['game_over', 'won', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
