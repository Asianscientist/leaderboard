from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import HttpResponse
import redis, json
from datetime import datetime
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserOutSerializer, UserSerializer,GameSerializerModel, SubmissionSerializer
from rest_framework.viewsets import ViewSet
from rest_framework import response
from django.contrib.auth import login, logout
from rest_framework.permissions import AllowAny
from .models import GamesModel
from rest_framework import exceptions
from . import display_players
from .serializers import LoginSerializer, UserSerializer

class SessionViewSet(ViewSet):
    permission_classes = (AllowAny,)

    def list(self, request):
        if not request.user.is_authenticated:
            raise exceptions.NotAuthenticated()
        serializer = UserSerializer(request.user)
        return response.Response(data=serializer.data)

    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return response.Response(UserSerializer(user).data, status=201)

    def delete(self, request):
        logout(request)
        return response.Response(status=204)


class CreateUser(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = UserSerializer
    queryset = User.objects.all()


games = ["Ping Pong", "Tennis", "Valleyball", "Soccer"]
r = redis.Redis(host='localhost', port=6379,  password='mysecret24')

@api_view(['GET'])
def get_games(request):
    games=GamesModel.objects.all()
    serializer=GameSerializerModel(games, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])  
def submit_results(request):
    serializer=SubmissionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user=User.objects.get(username=request.user.username)
    
    r.zadd(
    serializer.data.get('game_name'),
    {
        user.username:serializer.data.get('score'),
        
    })
    return Response({"ms":'hello'})


@api_view(['get'])
@permission_classes([IsAuthenticated,])  
def display_top_users(request):
    games=GamesModel.objects.all()
    top_results={}
    for x in games:
        data=r.zrevrange(x.name, 0, 2, withscores=True)
        top_results[x.name]=data
    return Response({"top_results":top_results}) 


@api_view(['get'])
@permission_classes([IsAuthenticated,])
def display_top_players(request):
    leaders=display_players.players(GamesModel, r)
    return Response({"user_rankings":dict(sorted(leaders.items(), key=lambda item: item[1], reverse=True))}) 

class HelloApiView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        return Response({"ms":"message"})
    
@api_view(['get'])
@permission_classes([IsAuthenticated,])
def display_weekly_report(request):
    data=r.hgetall("weekly_report")
    print(data)
    return Response({'weekly_report':'hello'})

