from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from users.models import Profile
from django.db.models.signals import post_save


# 회원들을 초대할 그룹 테이블 작성
class Group(models.Model):
    # 그룹명
    groupcode = models.CharField(max_length=10,default='wrong')
    title = models.CharField(max_length=10,null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author_group')
    member = models.ManyToManyField(Profile, related_name='member_group', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    memberinvite = models.ManyToManyField(Profile, related_name='invited', blank=True)


#청소주기, 방이름, 방크기, history 목록, 담당자
class Room(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE,related_name="group_room")
    manager = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_room')
    title = models.CharField(max_length=10,default="")
    size = models.IntegerField(default=1)
    period = models.IntegerField(default=3)
    last_history = models.ForeignKey("History",on_delete=models.SET_NULL,null=True,related_name="history_room") 

class History(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE,related_name="room_history")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_history')
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    event = models.IntegerField(default=0) #0: 청소 1: 건의 2: 불만
    image = models.ImageField(null=True,upload_to ='post/')
    text = models.CharField(max_length=300,default="")

class Statics(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="profile_statics")
    room = models.ForeignKey(Room, on_delete=models.CASCADE,related_name="room_statics")
    date = models.DateField(auto_now=True)
    score = models.IntegerField(default=0)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["user","room"],name="statics_usergroup_unique")]
    def __str__(self):
        return f"방{self.room}의 유저{self.user}의 점수"

