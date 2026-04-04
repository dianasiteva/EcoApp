from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class AppUserModelTest(TestCase):
    def test_create_user_with_email(self):
        user = UserModel.objects.create_user(email='test@test.com', password='pass1234!')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email_raises(self):
        with self.assertRaises(ValueError):
            UserModel.objects.create_user(email='', password='pass1234!')

    def test_str_returns_email(self):
        user = UserModel.objects.create_user(email='diana@test.com', password='pass1234!')
        self.assertEqual(str(user), 'diana@test.com')

    def test_create_superuser_flags(self):
        user = UserModel.objects.create_superuser(email='super@test.com', password='pass1234!')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_email_is_normalized(self):
        user = UserModel.objects.create_user(email='User@TEST.COM', password='pass1234!')
        self.assertEqual(user.email, 'User@test.com')


class RegisterViewTest(TestCase):
    def test_register_page_loads(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_creates_user(self):
        self.client.post(reverse('accounts:register'), {
            'email': 'newuser@test.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertTrue(UserModel.objects.filter(email='newuser@test.com').exists())

    def test_register_redirects_to_login(self):
        response = self.client.post(reverse('accounts:register'), {
            'email': 'newuser2@test.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertRedirects(response, reverse('accounts:login'))

    def test_register_invalid_mismatched_passwords(self):
        self.client.post(reverse('accounts:register'), {
            'email': 'bad@test.com',
            'password1': 'StrongPass123!',
            'password2': 'WrongPass456!',
        })
        self.assertFalse(UserModel.objects.filter(email='bad@test.com').exists())


class ProfileDetailViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='user@test.com', password='pass1234!')

    def test_profile_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('accounts:details'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response['Location'])

    def test_profile_loads_for_logged_in_user(self):
        self.client.login(email='user@test.com', password='pass1234!')
        response = self.client.get(reverse('accounts:details'))
        self.assertEqual(response.status_code, 200)

    def test_profile_shows_own_user_object(self):
        self.client.login(email='user@test.com', password='pass1234!')
        response = self.client.get(reverse('accounts:details'))
        self.assertEqual(response.context['object'], self.user)
