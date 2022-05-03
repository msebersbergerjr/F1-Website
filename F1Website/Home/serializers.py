from dataclasses import fields
from rest_framework import serializers
from .models import Race_History

class Race_History_Serializers(serializers.ModelSerializer):
    class Meta:
        model = Race_History
        fields = ('season','round','circuit_id','date','team_id','position','points','status')