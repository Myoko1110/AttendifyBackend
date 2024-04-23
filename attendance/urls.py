from django.urls import path

from attendance import views

urlpatterns = [
    path('', views.AttendanceView.as_view(), name='member'),
    path('response/', views.ResponseView.as_view(), name='response'),
    path('member/<int:id>/', views.AttendanceMemberView.as_view()),
    path('part/<str:part>/', views.AttendancePartView.as_view()),
]
