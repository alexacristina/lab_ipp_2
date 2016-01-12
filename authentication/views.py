from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.contrib.auth import hashers
from django.http import HttpResponse
from django.http import JsonResponse

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from authentication.serializers import UserSerializer
from authentication.serializers import ChangePasswordSerializer
from authentication.permissions import IsAuthenticatedOrCreate
from authentication.serializers import GroupSerializer


class UserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrCreate,]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.data
        u, created = User.objects.get_or_create(username=data['username'])
        u.set_password(data['password'])
        u.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @detail_route(methods=['get'], permission_classes=[IsAuthenticated])
    def last_login(self, request, pk):
        user = self.get_object()
        last_user_login = user.last_login
        return Response({'username': user.username,
                        'last_login' : last_user_login })

    @detail_route(methods=['post'])
    def change_password(self, request, pk):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request':request})
        user = self.get_object()

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'username': user.username})
        else:
            return Response({'invalid': 'invalid'})

class GroupViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer