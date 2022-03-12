from django.urls import path, include

urlpatterns = [
    path('auth/', include('api.urls.urls_user')),
    path('budget/', include('api.urls.urls_budget')),
    path('', include('api.urls.urls_main'))
]