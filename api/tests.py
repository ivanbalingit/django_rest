from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.backends import TokenBackend

class APITest(TestCase):
    def setUp(self):
        self.test_username = "user_test"
        self.test_email = "email@email.com"
        self.test_password = "password01"

        self.user0 = User.objects.create(username=self.test_username, email=self.test_email)
        self.user0.set_password(self.test_password)
        self.user0.save()
    
    def tearDown(self):
        self.user0.delete()

    def test_create_account(self):
        user_details = {
            'username': "user01",
            'email': "email@email.com",
            'password': "password01",
        }

        response = self.client.post('/auth/signup/', user_details, format='json')
        user_id  = response.data['data']['id']
        user     = User.objects.get(id=user_id)

        self.assertEqual(response.data['message'], "Signup successful!")
        self.assertEqual(response.data['data']['username'], user_details['username'])
        self.assertEqual(response.data['data']['email'], user_details['email'])
        self.assertEqual(user.username, user_details['username'])
        self.assertEqual(user.email, user_details['email'])

    def test_login(self):
        user_details = {
            'username': self.test_username,
            'password': self.test_password,
        }

        response   = self.client.post('/auth/login/', user_details, format='json')
        token      = response.data['access']
        token_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
        user_login = User.objects.get(id=token_data['user_id'])

        self.assertEqual(self.user0, user_login)