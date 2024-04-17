from django.urls import path

from schedule import views

urlpatterns = [
    path('', views.ScheduleView.as_view(), name='schedule'),
]
