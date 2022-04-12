from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('current/constructors/', views.constructor_home),
    path('constructor/<str:pk>/', views.constructor_page),
    path('<str:pk>/', views.driver_page),
    path('getracehistory/', views.get_race_history)
]