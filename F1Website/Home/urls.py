from django.urls import path
from Home import views

urlpatterns = [
    path('', views.landing),
    path('drivers/<str:pk>/', views.drivers_page),
    path('driver/<str:pk>/', views.driver_page),
    path('driver/<str:pk>/ajax/race-history/', views.get_race_history),
    path('driver/<str:pk>/ajax/driver-chart/', views.get_driver_chart),
    path('teams/', views.teams_page),
    path('teams/ajax/teams-page', views.teams_page_ajax),
    path('teams/ajax/team-points-season-chart', views.get_season_team_points_chart),
    path('teams/<str:pk>/', views.team_page),
    path('results/<str:pk>', views.results_page),
]