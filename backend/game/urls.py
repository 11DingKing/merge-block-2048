from django.urls import path
from . import views

urlpatterns = [
    path('api/new-game/', views.new_game, name='new_game'),
    path('api/move/', views.move, name='move'),
    path('api/undo/', views.undo, name='undo'),
]
