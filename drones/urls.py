from django.urls import path

from .views import *

urlpatterns = [
    path('drone-categories/', DroneCategoryList.as_view(), name=DroneCategoryList.name),
    path('drone-categories/<int:pk>', DroneCategoryDetail.as_view(), name=DroneCategoryDetail.name),
    path('drones/', DroneList.as_view(), name=DroneList.name),
    path('drones/<int:pk>', DroneDetail.as_view(), name=DroneDetail.name),
    path('pilots/', PilotList.as_view(), name=PilotList.name),
    path('pilots/<int:pk>', PilotDetail.as_view(), name=PilotDetail.name),
    path('competitions/', CompetitionList.as_view(), name=CompetitionList.name),
    path('competitions/<int:pk>', CompetitionDetail.as_view(), name=CompetitionDetail.name),
    path('', ApiRoot.as_view(), name=ApiRoot.name)

]
