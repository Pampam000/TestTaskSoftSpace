from django.test import TestCase
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APIClient

from ..models import User


class UserCreateTestCase(TestCase):
    staff_user_data = {
        'username': 'staff_user',
        'password': 'StrongPassword123!',
        'is_staff': True
    }
    test_user_data = {
        'username': 'test_user',
        'password': 'StrongPassword123!'
    }

    new_user_data = {
        'username': 'new_user',
        'password': 'StrongPassword123!'
    }

    def setUp(self):
        self.client = APIClient()

        self.staff_user = User.objects.create_user(**self.staff_user_data)
        self.test_user = User.objects.create_user(**self.test_user_data)
        self.user_access, self.staff_access = self.get_tokens()

    def get_tokens(self):
        url = reverse('token_create')
        response: Response = self.client.post(url, self.test_user_data,
                                              format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        response2: Response = self.client.post(url, self.staff_user_data,
                                               format='json')

        return response.data['access'], response2.data['access']

    def test_unauthorized_put(self):
        url = reverse('users-detail', args=[self.test_user.id])
        response: Response = self.client.put(url)
        self.assertEqual(response.status_code, 401)


    def test_unauthorized_list(self):
        url = reverse('users-list')
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_unauthorized_retrieve(self):
        url = reverse('users-detail', args=[self.test_user.id])
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_unauthorized_patch(self):
        url = reverse('users-detail', args=[self.test_user.id])
        response: Response = self.client.patch(url)
        self.assertEqual(response.status_code, 401)

    def test_unauthorized_delete(self):
        url = reverse('users-detail', args=[self.test_user.id])
        response: Response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    def test_success_create_user(self):
        url = reverse('users-list')
        response: Response = self.client.post(url,
                                              data=self.new_user_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.filter(is_active=True).count(), 3)
        self.assertTrue('password' not in response.data)

    def test_put(self):
        url = reverse('users-detail', args=[self.test_user.id])
        headers = {"Authorization": f"Bearer {self.user_access}"}
        response: Response = self.client.put(url, headers=headers)
        self.assertEqual(response.status_code, 405)

    def test_get_me(self):
        url = reverse('users-detail', args=[self.test_user.id])
        headers = {"Authorization": f"Bearer {self.user_access}"}
        response: Response = self.client.get(url, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('password' not in response.data)

    def test_get_another_user(self):
        url = reverse('users-detail', args=[self.staff_user.id])
        headers = {"Authorization": f"Bearer {self.user_access}"}
        response: Response = self.client.get(url, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('password' not in response.data)

    def test_patch_me(self):
        url = reverse('users-detail', args=[self.test_user.id])
        headers = {"Authorization": f"Bearer {self.user_access}"}
        data = {'first_name': 'name'}
        response: Response = self.client.patch(url, headers=headers,
                                               data=data)

        self.test_user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.test_user.first_name, data['first_name'])
        self.assertTrue('password' not in response.data)

    def test_patch_another_user(self):
        url = reverse('users-detail', args=[self.staff_user.id])
        headers = {"Authorization": f"Bearer {self.user_access}"}
        data = {'first_name': 'name'}
        response: Response = self.client.patch(url, headers=headers,
                                               data=data)
        self.test_user.refresh_from_db()
        self.assertEqual(response.status_code, 403)

    def test_staff_patch_another_user(self):
        url = reverse('users-detail', args=[self.test_user.id])
        headers = {"Authorization": f"Bearer {self.staff_access}"}
        data = {'first_name': 'name1'}
        response: Response = self.client.patch(url, headers=headers,
                                               data=data)
        self.test_user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.test_user.first_name, data['first_name'])
        self.assertTrue('password' not in response.data)

    def test_delete_another_user(self):
        url = reverse('users-detail', args=[self.staff_user.id])
        headers = {"Authorization": f"Bearer {self.user_access}"}

        response: Response = self.client.delete(url, headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_delete_me(self):
        url = reverse('users-detail', args=[self.test_user.id])
        headers = {"Authorization": f"Bearer {self.user_access}"}
        response: Response = self.client.delete(url, headers=headers)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.filter(is_active=True).count(), 1)

    def test_staff_delete_another_user(self):
        url = reverse('users-detail', args=[self.test_user.id])
        headers = {"Authorization": f"Bearer {self.staff_access}"}
        response: Response = self.client.delete(url, headers=headers)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.filter(is_active=True).count(), 1)
