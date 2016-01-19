from rest_framework.permissions import BasePermission
from bucketlist.models import BucketListItem


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
    	import ipdb
    	# ipdb.set_trace()
        if isinstance(obj, BucketListItem):
            return obj.bucketlist.created_by == request.user

        return obj.created_by == request.user