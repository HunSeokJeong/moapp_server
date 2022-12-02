from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.views    import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models  import Token
from .models import Group,Room,History,Statics
from users.models import Profile,User
from rest_framework.response import Response
from django.db.models import Sum
from .serializer import GroupCreateSerializer, GroupSerializer, \
    RoomSerializer, HistorySerializer,HistoryCreateSerializer,\
        ProfileSerializer,UserSerializer,StaticsSerializer

from .permissions import CustomOnly
import datetime
import pytz

# Create your views here.

@permission_classes([IsAuthenticated])
class GroupAPI(APIView):
    # def get(self,request):
    #     members = request.user
    def post(self,request):
        serializer= GroupCreateSerializer(data=request.data)
        if serializer.is_valid():
            group=serializer.save(author=request.user.user_profile)
            group.member.add(request.user.user_profile)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        query = request.user.user_profile.member_group.all()
        serializer = GroupSerializer(query,many=True)
        return Response({"group_list":serializer.data},status=status.HTTP_200_OK)

#그룹초대요청확인
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def showmeminvite(request):
    group=Group.objects.get(pk=request.GET['group'])
    return Response({"member_list":ProfileSerializer(group.memberinvite.all(),many=True).data},status=status.HTTP_200_OK)

#그룹 멤버 확인
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def showmem(request):
    group=Group.objects.get(pk=request.GET['group'])
    return Response({"member_list":ProfileSerializer(group.member.all(),many=True).data},status=status.HTTP_200_OK)

#초대요청 보내기
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def requestinvite(request):
    group=Group.objects.get(groupcode=request.data.get('groupcode'))
    group.memberinvite.add(request.user.user_profile)
    group.save()
    serializer= GroupSerializer(group)
    print(serializer.data)
    return Response(serializer.data,status=status.HTTP_200_OK)

#코드로 그룹에 들어가기
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def getintogroup(request):
    group=Group.objects.get(groupcode=request.data.get('groupcode'))
    group.member.add(request.user.user_profile)
    group.save()
    serializer= GroupSerializer(group)
    print(serializer.data)
    return Response(serializer.data,status=status.HTTP_200_OK)

#멤버 추가
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addmember(request):
    group=Group.objects.get(pk=request.data.get('group'))
    # if group.author!=request.user.user_profile :
    #     return Response({"error":"그룹에 관한 권한이 없습니다."},status=status.HTTP_406_NOT_ACCEPTABLE)
    newmem=Profile.objects.get(pk=request.data.get("newmember"))
    group.member.add(newmem)
    group.memberinvite.remove(newmem)
    group.save()
    return Response(GroupSerializer(group).data,status=status.HTTP_200_OK)

@permission_classes([IsAuthenticated])
class RoomAPI(APIView):
    # def get(self,request):
    #     members = request.user
    def post(self,request):
        serializer= RoomSerializer(data=request.data)
        if serializer.is_valid():
            group=Group.objects.get(pk=request.data.get('group'))
            if group.author!=request.user.user_profile :
                return Response({"error":"그룹에 관한 권한이 없습니다."},status=status.HTTP_406_NOT_ACCEPTABLE)

            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        group = Group.objects.get(pk=request.GET['group'])
        rooms = group.group_room.all()
        serializer = RoomSerializer(rooms,many=True)
        return Response({"roomlist":serializer.data},status=status.HTTP_200_OK)


class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    permission_classes = [CustomOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['room']
    def get_serializer_class(self):
        if self.action == 'create':
            return HistoryCreateSerializer
        elif self.action == 'list' or 'retrieve':
            return HistorySerializer
        return HistoryCreateSerializer
    def perform_create(self,serializer):
        history = serializer.save(author=self.request.user.user_profile)
        if self.request.data.get('event')=='0' :
            print("ok")
            room=Room.objects.get(id=self.request.data.get('room'))
            room.last_history = history
            room.save()

    def list(self, request, *args, **kwargs):
        historys = History.objects.all()
        historys = self.filter_queryset(historys).order_by('-create_date')

        serializer = self.get_serializer(historys, many=True)
        return Response({"listhistory":serializer.data}, status=status.HTTP_200_OK)



def get_static(room, user, period):
    histories = History.objects.filter(room=room,author=user,event=0)
    border_date = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)-datetime.timedelta(days=period) 
    sum = 0
    for obj in histories:
        if(obj.create_date> border_date):
            sum+=obj.room.size
    print(room,user,sum)
    Statics.objects.update_or_create(
        room=room,
        user=user,
        defaults={"score":sum}
    )



@api_view(['POST'])
def updatestatic(request):
    group=Group.objects.get(pk=request.data.get("group"))
    for room in group.group_room.all():
        for member in group.member.all():
            print(room,member)
            get_static(room,member,30)

    # get_static(2,1,3)
    return Response(status=status.HTTP_200_OK)


class StaticsViewSet(viewsets.ModelViewSet):
    queryset = Statics.objects.all()
    serializer_class = StaticsSerializer
    filter_backends = [DjangoFilterBackend] # 👈 DjangoFilterBackend 지정
    filterset_fields = ['room', 'user'] # 👈 filtering 기능을 사용할 field 입력

    def list(self, request, *args, **kwargs):
        statics = Statics.objects.all()
        statics = self.filter_queryset(statics)

        serializer = self.get_serializer(statics, many=True)
        return Response({"liststatics":serializer.data}, status=status.HTTP_200_OK)
