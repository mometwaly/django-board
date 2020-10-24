from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="index"),
    path('boards/<board_id>/', views.board_topics, name="board_topic"),
    path('boards/<board_id>/new', views.new_topic, name="new_topic"),
    path('boards/<board_id>/topics/<topic_id>', views.topic_posts, name="topic_posts"),
    path('boards/<board_id>/topics/<topic_id>/reply/', views.reply, name="reply")
    ]