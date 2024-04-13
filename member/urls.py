from django.urls import path

from member import views

urlpatterns = [
    path('', views.MemberView.as_view(), name='member'),
]
