from django.shortcuts import render
from .serializers import UserSerializer
from rest_framework.views import APIView
from .models import User
from rest_framework import generics

# Create your views here.

class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializers_class = UserSerializer