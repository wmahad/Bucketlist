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
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserSignInView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        data = request.data
        try:
            user = User.objects.get(username=data.get('username'))
            if user.password != data.get('password'):
                return Response(
                    message='Wrong credentials',
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except:
            return Response(
                message='No default user, please create one',
                status=status.HTTP_404_NOT_FOUND
            )

        token = Token.objects.get_or_create(user=user)

        return Response({'token': token[0].key, 'id':token[0].user_id})


class BucketDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated,)

    queryset = BucketList.objects.all()
    serializer_class = BucketListSerializer

    


class BucketListView(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated,)

    queryset = BucketList.objects.all()
    serializer_class = BucketListSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return BucketList.objects.all().filter(created_by=user)


class BucketListItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated,)

    queryset = BucketListItem.objects.all()
    serializer_class = BucketListItemSerializer


class BucketListItemView(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated,)

    queryset = BucketListItem.objects.all()
    serializer_class = BucketListItemSerializer


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated,)

    def get(self, request, format=None):
        request.auth.delete()
        return Response({'suceess': 'Logged out'})
