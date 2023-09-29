from ..models import User
from django.test import TestCase

from rest_framework.exceptions import ValidationError as DRFValidationError
from ..serializers import UserSerializer


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.valid_user_data = {
            'username': 'testuser',
            'password': 'StrongPassword123!',
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
        }

    def test_user_serializer_create(self):
        serializer = UserSerializer(data=self.valid_user_data)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()

        self.assertEqual(user.username, self.valid_user_data['username'])
        self.assertEqual(user.email, self.valid_user_data['email'])
        self.assertEqual(user.first_name, self.valid_user_data['first_name'])
        self.assertEqual(user.last_name, self.valid_user_data['last_name'])

        # Проверяем, что пароль хэширован
        self.assertTrue(user.check_password(self.valid_user_data['password']))


    def test_password_validation(self):
        # Неверный пароль
        invalid_user_data = self.valid_user_data.copy()
        invalid_user_data['password'] = 'short'

        serializer = UserSerializer(data=invalid_user_data)
        with self.assertRaises(DRFValidationError):
            serializer.is_valid(raise_exception=True)


        # Верный пароль
        valid_user_data = self.valid_user_data.copy()
        valid_user_data['password'] = 'StrongPassword123!'

        serializer = UserSerializer(data=valid_user_data)
        self.assertTrue(serializer.is_valid())

    def test_user_serializer_update(self):
        user = User.objects.create(**self.valid_user_data)

        updated_data = {
            'username': 'updateduser',
            'password': 'UpdatedPassword456!',
            'email': 'updated@example.com',
            'first_name': 'UpdatedFirst',
            'last_name': 'UpdatedLast',
        }

        serializer = UserSerializer(user, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid())

        updated_user = serializer.save()

        self.assertEqual(updated_user.username, updated_data['username'])
        self.assertEqual(updated_user.email, updated_data['email'])
        self.assertEqual(updated_user.first_name, updated_data['first_name'])
        self.assertEqual(updated_user.last_name, updated_data['last_name'])

        # Проверяем, что пароль хэширован
        self.assertTrue(updated_user.check_password(updated_data['password']))
