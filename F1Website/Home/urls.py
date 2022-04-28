from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing),
    path('lineup/<str:pk>/', views.lineup_page),
    path('<str:pk>/', views.driver_page),
]