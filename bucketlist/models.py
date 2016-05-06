from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class BucketList(models.Model):  # on_delete=models.CASCADE
    """Modal class for bucketlist"""
    name = models.CharField(blank=False, unique=True, max_length=70)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)

    def __str__(self):
        """The str method for bucketlist"""
        return 'BucketList : {}'.format(self.name)


class BucketListItem(models.Model):
    """Modal class for bucketlist-item"""
    name = models.CharField(blank=False, unique=True, max_length=70)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    done = models.BooleanField(default=False)
    bucketlist = models.ForeignKey(
        BucketList, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        """The str method for bucketlist-item"""
        return 'Item : {}'.format(self.name)
