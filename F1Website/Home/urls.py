from django.urls import path
from Home import views

urlpatterns = [
    path('', views.landing),
    path('lineup/<str:pk>/', views.lineup_page),
    path('driver/<str:pk>/', views.driver_page),
    path('driver/<str:pk>/ajax/race-history/', views.get_race_history),
    # path("ajax/circuit/", getCircuit, name='get_circuit'),
    # path("ajax/date/", getDate, name='get_date'),
    # path("ajax/team/", getTeam, name='get_team'),
    # path("ajax/position/", getPosition, name='get_position'),
    # path("ajax/status/", getStatus, name='get_status'),
]