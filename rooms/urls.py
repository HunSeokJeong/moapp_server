from django.urls import path,include
from .views import GroupAPI,requestinvite,addmember,RoomAPI,showmeminvite\
    ,showmem, HistoryViewSet,updatestatic,StaticsViewSet,getintogroup
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('history',HistoryViewSet)

urlpatterns = [
    path("group/",GroupAPI.as_view()),
    path("requestinvite/",requestinvite),
    path("addmember/",addmember),
    path("showmeminvite/",showmeminvite),
    path("showmem/",showmem),
    path("updatestatic/",updatestatic),
    path("getintogroup/",getintogroup),
    path("room/",RoomAPI.as_view()),
    path("statics/",StaticsViewSet.as_view({'get':'list'})),
    path("",include(router.urls)),
]