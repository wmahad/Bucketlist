from rest_framework.permissions import BasePermission
from bucketlist.models import BucketListItem


class IsOwnerOrReadOnly(BasePermission):
	"""Setting permission class to isOwner or read only"""
    def has_object_permission(self, request, view, obj):
    	# Setting permissions for who modifies the bucketlist
        if isinstance(obj, BucketListItem):
            return obj.bucketlist.created_by == request.user

        return obj.created_by == request.user