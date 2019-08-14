from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .serializer import *


# Create your views here.

class DroneCategoryList(generics.ListCreateAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = 'dronecategory-list'
    filter_fields = (
        'name',
    )
    search_fields = (
        '^name',
    )
    ordering_fields = (
        'name',
    )


class DroneCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = 'dronecategory-detail'


class DroneList(generics.ListCreateAPIView):
    # queryset 혹은 get_queryset() 오버라이딩
    queryset = Drone.objects.all()
    # serializer_class 혹은 get_serializer_class() 오버라이딩
    serializer_class = DroneSerializer
    # lookup_field : 개별 모델 인스턴스의 객체를 조회할 때 사용하는 필드(default : pk)
    # Hyperlinked -> API View(name = 'drone-list') & serializer(slug_field='name') 설정
    name = 'drone-list'
    filter_fields = (
        'name',
        'drone_category',
        'manufacturing_date',
        'has_it_competed',
    )
    search_fields = (
        '^name',
    )
    ordering_fields = (
        'name',
        'manufacturing_date',
    )


class DroneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = 'drone-detail'


class PilotList(generics.ListCreateAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = 'pilot-list'
    filter_fields = (
        'name',
        'gender',
        'races_count',
    )
    search_fields = (
        '^name',
    )
    ordering_fields = (
        'name',
        'races_count'
    )


class PilotDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = 'pilot-detail'


# Customizing filter
class CompetitionFilter(filters.FilterSet):
    from_achievement_date = DateTimeFilter(field_name='distance_achievement_date', lookup_expr='gte')
    to_achievement_date = DateTimeFilter(field_name='distance_achievement_date', lookup_expr='lte')
    min_distance_in_feet = NumberFilter(field_name='distance_in_feet', lookup_expr='gte')
    max_distance_in_feet = NumberFilter(field_name='distance_in_feet', lookup_expr='lte')
    drone_name = AllValuesFilter(field_name='drone__name')  # drone.name
    pilot_name = AllValuesFilter(field_name='pilot__name')  # pilot.name

    class Meta:
        model = Competition
        fields = (
            'distance_in_feet',
            'from_achievement_date',
            'to_achievement_date',
            'min_distance_in_feet',
            'max_distance_in_feet',
            'drone_name',
            'pilot_name',
        )


class CompetitionList(generics.ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = 'competition-list'
    filter_class = CompetitionFilter
    ordering_fields = (
        'distance_in_feet',
        'distance_achievement_date',
    )


class CompetitionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = 'competition-detail'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            # resverse = URL resolver(확인자) 함수 -> 해당 뷰의 url 반환
            # key = view의 이름
            # value = reverse()를 이용해 해당 view에 대한 url 생성
            # -> return
            'drone-categories': reverse(DroneCategoryList.name, request=request),
            'drones': reverse(DroneList.name, request=request),
            'pilots': reverse(PilotList.name, request=request),
            'competitions': reverse(CompetitionList.name, request=request)
        })
