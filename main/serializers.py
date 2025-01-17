from rest_framework import serializers

from main.models import Team

class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = ('team_name', 'team_stadium', 'team_country')