from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from bucketlist.models import BucketList, BucketListItem

from faker import Factory

fake = Factory.create()

class UserTests(APITestCase):
	"""
	Tests to do with user registration and login
	"""
	def setUp(self):
		self.username = fake.user_name()
		self.password = fake.password()
		self.user = User.objects.create_user(
	        username=self.username,  password=self.password)

	def tearDown(self):
	    """Delete the user modal after use"""
	    del self.user


	def test_user_creation_succeeds(self):
	    """
	    tests whether a user gets created when new user signs up
	    """
	    url = reverse('auth_signup')
	    user_name = fake.user_name()
	    data = {'username': user_name, 'password':fake.password()}
	    response = self.client.post(url, data)
	    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
	    self.assertEqual(response.data.get('username'), user_name)

	def test_user_creation_fails_when_same_user_registers(self):
	    """
	    tests whether user creation fails when same user tries to register
	    """
	    url = reverse('auth_signup')
	    data = {'username': self.username, 'password':self.password}
	    response = self.client.post(url, data)
	    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
	    self.assertNotEqual(
	    	response.data.get('username'), "A user with that username already exists.")


	def test_users_can_login_when_they_provide_correct_info(self):
		"""tests whether user can login when he provides the right info"""
		url = reverse('auth_signin')
		data = {'username': self.username, 'password':self.password}
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn("token", response.data)


	def test_users_can_not_login_when_they_provide_wrong_info(self):
		"""tests whether user can't login when he provides wrong info"""
		url = reverse('auth_signin')
		self.username = fake.user_name(); 
		data = {'username': self.username, 'password':self.password}
		response = self.client.post(url, data)
		self.assertNotIn("token", response.data)
		self.assertIn(
			"Unable to login with provided credentials.", 
			response.data.get('non_field_errors'))
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BucketListTests(APITestCase):
	"""
	Tests to do with BucketList creation  and deletion
	"""
	def setUp(self):
		"""Set up data specific to the test cases for bucketlist"""
		# bucketlist specific details
		self.name = fake.first_name()
		# create a user
		self.username = fake.user_name();
		self.password = fake.password();
		self.user = User.objects.create_user(
	        username=self.username,  password=self.password)

		self.bucketlist = BucketList.objects.create(name=self.name, created_by=self.user)

		# login a user 
		url = reverse('auth_signin')
		data = {'username': self.username, 'password':self.password}
		self.response = self.client.post(url, data)
		self.token = self.response.data.get('token')

	def tearDown(self):
	    """Delete the user modal after use"""
	    del self.user
	    del self.bucketlist
	    del self.token
	    del self.response

	def test_bucketlist_creation_succeeds_when_right_info_is_provided(self):		
		"""tests whether bucketlist gets created when he provides the right info"""
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
		self.name = fake.first_name()
		data = {'name': self.name}
		url = reverse('all_bucketlists') 
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data.get('name'), self.name)


	def test_bucketlist_creation_fails_when_wrong_info_is_provided(self):		
		"""tests whether bucketlist isn't created when he provides the right info"""
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
		data = {'name': self.name}
		url = reverse('all_bucketlists') 
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertNotEqual(response.data.get('name'), self.name)


	def test_bucketlist_deletion_succeeds(self):		
		"""tests whether bucketlist gets deleted """
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)	
		bucketlist = BucketList.objects.get(name=self.name)

		url = "/api/bucketlists/{}/".format(bucketlist.id)
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

	def test_bucketlist_update_succeeds(self):		
		"""tests whether bucketlist gets updated"""
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
		bucketlist = BucketList.objects.get(name=self.name)
		self.name = fake.first_name()
		data = {'name':self.name, 'id':bucketlist.id}
		url = "/api/bucketlists/{}/".format(bucketlist.id)
		response = self.client.put(url, data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data.get('name'), self.name)



class BucketListItemTests(APITestCase):
	"""
	Tests to do with BucketList creation  and deletion
	"""
	def setUp(self):
		"""setup bucketlist item specific data"""
		# bucketlist specific details
		self.name = fake.first_name()
		# bucketlist item specific details
		self.item = fake.last_name()
		# create a user
		self.username = fake.user_name();
		self.password = fake.password();
		self.user = User.objects.create_user(
	        username=self.username,  password=self.password)

		self.bucketlist = BucketList.objects.create(name=self.name, created_by=self.user)

		self.bucketlist_item = BucketListItem.objects.create(name=self.item, bucketlist=self.bucketlist)

		# login a user 
		url = reverse('auth_signin')
		data = {'username': self.username, 'password':self.password}
		self.response = self.client.post(url, data)
		self.token = self.response.data.get('token')

	def tearDown(self):
	    """Delete the specificsafter use"""
	    del self.user
	    del self.bucketlist
	    del self.token
	    del self.bucketlist_item
	    del self.response

	def test_bucketlist_item_creation_succeeds_when_right_info_is_provided(self):		
		"""tests whether bucketlist_item is created when he provides the right info"""
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
		self.item = fake.last_name()
		data = {'name': self.item, 'bucketlist':self.bucketlist.id}
		url = "/api/bucketlists/{}/items/".format(self.bucketlist.id) 
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data.get('name'), self.item)


	def test_bucketlist_item_creation_fails_when_wrong_info_is_provided(self):		
		"""tests whether bucketlist_item doesn't get created when he provides the wrong info"""
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
		data = {'name': self.item, 'bucketlist':self.bucketlist.id}
		url = "/api/bucketlists/{}/items/".format(self.bucketlist.id) 
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertNotEqual(response.data.get('name'), self.name)


	def test_bucketlist_item_deletion_succeeds(self):		
		"""tests whether bucketlist_item gets deleted"""
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)	
		bucketlist = BucketList.objects.get(name=self.name)

		url = "/api/bucketlists/{0}/items/{1}/".format(
			self.bucketlist.id, self.bucketlist_item.id) 
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

	def test_bucketlist_item_update_succeeds(self):		
		"""tests whether bucketlist_item gets updated"""
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
		item = BucketListItem.objects.get(name=self.item)
		self.item = fake.last_name()
		data = {'name':self.item, 'bucketlist': item.bucketlist.id}
		url = "/api/bucketlists/{0}/items/{1}/".format(
			item.bucketlist.id, item.id)
		response = self.client.put(url, data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data.get('name'), self.item)
