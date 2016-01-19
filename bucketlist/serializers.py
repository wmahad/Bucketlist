from rest_framework import serializers
from django.contrib.auth.models import User
from bucketlist.models import BucketList, BucketListItem


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password')


class BucketListItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = BucketListItem
        fields = ('id', 'name', 'date_created',
                  'date_modified', 'done', 'bucketlist')
        read_only_fields = ('date_created', 'date_modified',)


class BucketListSerializer(serializers.ModelSerializer):

    items = BucketListItemSerializer(many=True, read_only=True)
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = BucketList
        fields = ('id', 'name', 'items', 'date_created',
                  'date_modified', 'created_by')
        read_only_fields = ( 'date_created', 'date_modified',
                            'items')
