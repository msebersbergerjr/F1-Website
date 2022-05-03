from django.urls import path
from Home import views

urlpatterns = [
    path('', views.landing),
    path('drivers/<str:pk>/', views.drivers_page),
    path('driver/<str:pk>/', views.driver_page),
    path('driver/<str:pk>/ajax/race-history/', views.get_race_history),
    path('teams/<str:pk>', views.teams_page),
    path('team/<str:pk>/', views.team_page),
]