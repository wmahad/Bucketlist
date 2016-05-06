from django.contrib.auth.models import User
from django.shortcuts import render
from bucketlist.models import BucketList, BucketListItem
from bucketlist.serializers import UserSerializer

from bucketlist.serializers import BucketListSerializer
from bucketlist.serializers import BucketListItemSerializer

from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from bucketlist.permissions import IsOwnerOrReadOnly

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status



class UserSignUpView(generics.CreateAPIView):
    """The view set for User sign up"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
      


class BucketDetailView(generics.RetrieveUpdateDestroyAPIView):
    """The view set for handling display of bucketlist details"""
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated,)

    queryset = BucketList.objects.all()
    serializer_class = BucketListSerializer

    


class BucketListView(generics.ListCreateAPIView):
    """The view set for bucketlist creation"""
    # Setting permission classes
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated,)

    queryset = BucketList.objects.all()
    serializer_class = BucketListSerializer

    def perform_create(self, serializer):
        """Method for handling the actual creation"""
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        """Modify query to display bucketlists for logged in user"""
        user = self.request.user
        return BucketList.objects.all().filter(created_by=user)


class BucketListItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """The view set for handling items display"""

    queryset = BucketListItem.objects.all()
    serializer_class = BucketListItemSerializer


class BucketListItemView(generics.ListCreateAPIView):
    """The view set foe handling item creation"""
    # Setting permission classes
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated,)

    queryset = BucketListItem.objects.all()
    serializer_class = BucketListItemSerializer

