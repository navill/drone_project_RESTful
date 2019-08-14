from rest_framework import serializers

from drones.models import DroneCategory, Drone, Competition, Pilot


class DroneCategorySerializer(serializers.HyperlinkedModelSerializer):
    """
    읽기 전용 일대 다 관계 정의
    DroneCategory - parent
        - child
        1.Drone(drone_category/related_name=drones),
        2.Drone(drone_category/related_name=drones),
        3.Drone(drone_category/related_name=drones),
    """
    # drones -> drone_category의 related name
    drones = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='drone-detail'
    )

    class Meta:
        model = DroneCategory
        fields = (
            'url', 'pk', 'name', 'drones'
        )


class DroneSerializer(serializers.HyperlinkedModelSerializer):
    # SlugRelatedField : 고유한 슬러그 속성을 갖는 읽기/쓰기 필드 -> 대상의 필드를 이용해 관계된 대상을 나타낼 때 사용
    # DroneCategory 의 name field 를 이용해 drone_category 를 나타낸다.
    drone_category = serializers.SlugRelatedField(queryset=DroneCategory.objects.all(), slug_field='name')

    class Meta:
        model = Drone
        fields = (
            'url', 'name', 'manufacturing_date', 'has_it_competed', 'inserted_timestamp', 'drone_category'
        )


class CompetitionSerializer(serializers.HyperlinkedModelSerializer):
    drone = DroneSerializer()

    class Meta:
        model = Competition
        fields = (
            'url', 'pk', 'distance_in_feet', 'distance_achievement_date', 'drone'
        )


class PilotSerializer(serializers.HyperlinkedModelSerializer):
    # related_name of Pilot.pilot(FK:competition) : competitions
    competitions = CompetitionSerializer(many=True, read_only=True)
    gender = serializers.ChoiceField(choices=Pilot.GENDER_CHOICES)
    gender_description = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = Pilot
        fields = (
            'url', 'name', 'gender', 'gender_description', 'races_count', 'inserted_timestamp', 'competitions'
        )


class PilotCompetitionSerializer(serializers.ModelSerializer):
    pilot = serializers.SlugRelatedField(queryset=Pilot.objects.all(), slug_field='name')
    drone = serializers.SlugRelatedField(queryset=Drone.objects.all(), slug_field='name')

    class Meta:
        model = Competition
        fields = (
            'url', 'pk', 'distance_in_feet', 'distance_achievement_date', 'pilot', 'drone'
        )
