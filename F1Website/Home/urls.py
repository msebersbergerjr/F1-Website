from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('<str:pk>/', views.driver_page),
    path('performence/', views.performence_histroy, name='performence')
]