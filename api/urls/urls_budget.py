from django.urls import path

from api.views import views_budget

urlpatterns = [
    path('', views_budget.budget.as_view()),
]