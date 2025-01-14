from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_notifications),
    path('/<int:pk>', views.notification_detail),
]