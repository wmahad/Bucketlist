from rest_framework import serializers
from django.contrib.auth.models import User
from bucketlist.models import BucketList, BucketListItem


class UserSerializer(serializers.ModelSerializer):
    """Serializer class for users"""
    class Meta:
        """Meta class that sets the modal(User) in use
        and fields to expose"""
        model = User
        fields = ('id', 'username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class BucketListItemSerializer(serializers.ModelSerializer):
    """Serialiser class for bucketlist item"""
    class Meta:
        """Meta class for setting modal to be used and fields"""
        model = BucketListItem
        fields = ('id', 'name', 'date_created',
                  'date_modified', 'done', 'bucketlist')
        # Setting read only fields for the bucketlist-item
        read_only_fields = ('date_created', 'date_modified',)


class BucketListSerializer(serializers.ModelSerializer):
    """Serialiser class for bucketlist"""

    items = BucketListItemSerializer(many=True, read_only=True)
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        """Setting modal to bucketlist and fields"""
        model = BucketList
        fields = ('id', 'name', 'items', 'date_created',
                  'date_modified', 'created_by')
        # Setting read only fields
        read_only_fields = ( 'date_created', 'date_modified',
                            'items')
