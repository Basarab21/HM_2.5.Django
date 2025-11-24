from django.urls import path
from . import views

urlpatterns = [
    path('guess/', views.guess_view, name='guess_game'),
    path('guess/reset/', views.reset_game_view, name='reset_game'),
]