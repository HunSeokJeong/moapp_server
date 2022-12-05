from rest_framework import serializers
from users.serializers import ProfileSerializer,UserSerializer
from .models import Group,Room,History,Statics
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.validators import UniqueValidator


class GroupCreateSerializer(serializers.ModelSerializer):
    groupcode = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Group.objects.all())]
    )
    class Meta:
        model = Group
        fields = ('groupcode','title','member')


class GroupSerializer(serializers.ModelSerializer):
    member = ProfileSerializer(read_only=True,many=True)
    memberinvite = ProfileSerializer(read_only=True,many=True)
    class Meta:
        model = Group
        fields = ('id','groupcode','title','member','memberinvite','author')



class HistoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ('room','event','image','text')

class HistorySerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    class Meta:
        model = History
        fields = ('id','room','author','create_date','modify_date','event','image','text')


class RoomSerializer(serializers.ModelSerializer):
    last_history= HistorySerializer(read_only=True)
    manager = ProfileSerializer(read_only=True)
    class Meta:
        model = Room
        fields = ('id','group','manager','title','size','period',"last_history")



class StaticsSerializer(serializers.ModelSerializer):
    user=ProfileSerializer(read_only=True)
    class Meta:
        model = Statics
        fields = ('user','room','date','score')

class GroupStaticsSerializer(serializers.Serializer):
    user=ProfileSerializer(read_only=True)
    total_score=serializers.IntegerField()
