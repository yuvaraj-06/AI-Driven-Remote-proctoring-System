from django.urls import path, include
from streamapp import views


urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add, name='add'),
    path('take', views.take, name='take'),
    path('quiz', views.quiz, name='quiz'),
    path('video_feed', views.video_feed, name='video_feed'),
    path('video_fee', views.video_fee, name='video_fee'),
    path('startexm', views.startexm, name='startexm'),
    path('record', views.record, name='record'),
    
    

    ]

