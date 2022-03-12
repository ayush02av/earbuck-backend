from django.urls import path

from api.views import views_main

urlpatterns = [
    path('dashboard/', views_main.dashboard.as_view()),
]