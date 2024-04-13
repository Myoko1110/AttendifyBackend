from django.urls import path

from auths import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('session/', views.SessionView.as_view(), name='session'),
]
