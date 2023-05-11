from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User,Verify

class SendVerificationCodeTest(APITestCase):
    
    def setUp(self):
        self.url = reverse('send_verification_code_view')
    def test_send_verification_code(self):
        email_info = {
            'email': 'test@test.com',
        }
        response = self.client.post(self.url, email_info, format='json')
        self.assertEqual(response.status_code, 200)
    
    def test_send_verification_code_blank_email(self):
        email_info = {
            'email': '',
        }
        response = self.client.post(self.url, email_info, format='json')
        self.assertEqual(response.status_code, 400)

    def test_send_verification_code_not_email(self):
        email_info = {
            'email': 'test',
        }
        response = self.client.post(self.url, email_info, format='json')
        self.assertEqual(response.status_code, 400)
        
    def test_send_verification_code_already_register_email(self):
        User.objects.create_user(email='test@test.com', password='password')
        email_info = {
            'email': 'test@test.com'
        }
        response = self.client.post(self.url, email_info, format='json')
        self.assertEqual(response.status_code, 400)
        
class RegisterUserTest(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('sign_up_view')
        self.verify = reverse('send_verification_code_view')
        self.email_info ={
            'email': 'testuser@example.com',
        }
        self.code = self.client.post(self.verify, self.email_info, format='json').data['verification_code']
    #성공했을떄
    def test_register(self):
        user_info = {
            'email': 'testuser@example.com',
            'password': 'password',
            'code': self.code,
        }
        response = self.client.post(self.url, user_info, format='json')
        self.assertEqual(response.status_code, 201)
        
    def test_register_incorrect_email(self):
        user_info = {
            'email': '',
            'password': 'password',
            'code': self.code,
        }
        response = self.client.post(self.url, user_info, format='json')
        self.assertEqual(response.status_code, 400)
    
    def test_register_incorrect_code(self):
        user_info = {
            'email': '',
            'password': 'password',
            'code': '',
        }
        response = self.client.post(self.url, user_info, format='json')
        self.assertEqual(response.status_code, 400)
        
    def test_register_incorrect_code_email(self):
        user_info = {
            'email': '123@123.com',
            'password': 'password',
            'code': '123456',
        }
        response = self.client.post(self.url, user_info, format='json')
        self.assertEqual(response.status_code, 404)
    
    def test_register_incorrect_blank_password(self):
        user_info = {
            'email': 'testuser@example.com',
            'password': '',
            'code': self.code,
        }
        response = self.client.post(self.url, user_info, format='json')
        self.assertEqual(response.status_code, 400)
    
class LoginUserTest(APITestCase):
    def setUp(self):
        self.data = {'email': 'john', 'password': 'johnpassword'}
        self.user = User.objects.create_user('john','johnpassword')
    
    def test_login(self):
        response = self.client.post(reverse('token_obtain_pair'), self.data)
        self.assertEqual(response.status_code, 200)
        
    