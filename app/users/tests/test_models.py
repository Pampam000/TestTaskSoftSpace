from django.test import TestCase

from ..models import User


class UserModelTestCase(TestCase):

    def test_delete_user(self):
        """
        Проверяем, что метод delete() устанавливает is_active в False
        """
        user = User.objects.create_user(
            username='usertodelete',
            email='user@edelete.com',
            password='Testpassword1&'
        )

        user.delete()
        self.assertFalse(user.is_active)
        self.assertEqual(User.objects.count(), 1)
