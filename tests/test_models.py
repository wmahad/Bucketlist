from django.test import TestCase

from faker import Factory
from django.contrib.auth.models import User
from bucketlist.models import BucketList, BucketListItem

fake = Factory.create()


class UserTests(TestCase):

    def setUp(self):
        self.username = fake.user_name()
        self.password = fake.password()
        self.user = User(
            username=self.username,  password=self.password, is_superuser=True)

    def tearDown(self):
        del self.user

    def test_super_user_created(self):
        self.assertIsInstance(self.user, User)


class BucketListTests(TestCase):

    def setUp(self):
        self.username = fake.user_name()
        self.password = fake.password()
        self.user = User(
            username=self.username,  password=self.password, is_superuser=True)
        self.name = fake.name()
        self.bucketlist = BucketList(name=self.name, created_by=self.user)

    def test_bucket_list_created(self):
        self.assertIsInstance(self.bucketlist, BucketList)

    def test_str_method(self):
        self.assertEqual(str(self.bucketlist),
                         "BucketList : {}".format(self.name))


class BucketListItemTests(TestCase):

    def setUp(self):
        self.i_name = fake.name()
        self.username = fake.user_name()
        self.password = fake.password()
        self.user = User(
            username=self.username,  password=self.password, is_superuser=True)
        self.name = fake.name()
        self.bucketlist = BucketList(name=self.name, created_by=self.user)
        self.b_item = BucketListItem(
            name=self.i_name, bucketlist=self.bucketlist)

    def test_bucket_list_item_created(self):
        self.assertIsInstance(self.b_item, BucketListItem)

    def test_str_method(self):
        self.assertEqual(str(self.b_item),
                         "Item : {}".format(self.i_name))
