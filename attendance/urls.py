from django.urls import path

from attendance import views

urlpatterns = [
    path('', views.AttendanceView.as_view(), name='member'),
    path('response/', views.ResponseView.as_view(), name='response'),
]
