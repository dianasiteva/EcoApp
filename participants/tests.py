import datetime
from unittest.mock import MagicMock

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from cities.models import Cities
from events.models import Event, Location, Role
from participants.choises import DistrictChoice
from participants.models import Participant, ParticipantEventRole
from participants.validators import plate_validator, validate_image

UserModel = get_user_model()


# ─── Validators ───────────────────────────────────────────────────────────────

class PlateValidatorTest(TestCase):
    def test_valid_plate(self):
        plate_validator('ABCD1234')  # should not raise

    def test_valid_plate_min_length(self):
        plate_validator('ABCD')  # 4 chars is ok

    def test_invalid_lowercase(self):
        with self.assertRaises(ValidationError):
            plate_validator('abcd1234')

    def test_invalid_too_short(self):
        with self.assertRaises(ValidationError):
            plate_validator('AB')

    def test_invalid_too_long(self):
        with self.assertRaises(ValidationError):
            plate_validator('ABCDEFGHI')  # 9 chars

    def test_invalid_special_chars(self):
        with self.assertRaises(ValidationError):
            plate_validator('AB-CD12')


class ValidateImageTest(TestCase):
    def _mock_file(self, name, size_mb):
        f = MagicMock()
        f.name = name
        f.size = size_mb * 1024 * 1024
        return f

    def test_valid_jpg(self):
        validate_image(self._mock_file('photo.jpg', 1))  # should not raise

    def test_valid_jpeg(self):
        validate_image(self._mock_file('photo.jpeg', 2))

    def test_valid_png(self):
        validate_image(self._mock_file('photo.png', 1))

    def test_invalid_extension_gif(self):
        with self.assertRaises(ValidationError):
            validate_image(self._mock_file('photo.gif', 1))

    def test_invalid_extension_bmp(self):
        with self.assertRaises(ValidationError):
            validate_image(self._mock_file('photo.bmp', 1))

    def test_file_too_large(self):
        with self.assertRaises(ValidationError):
            validate_image(self._mock_file('photo.jpg', 6))  # 6MB > 5MB limit

    def test_exactly_5mb_is_ok(self):
        f = MagicMock()
        f.name = 'photo.jpg'
        f.size = 5 * 1024 * 1024
        validate_image(f)  # should not raise


# ─── Models ───────────────────────────────────────────────────────────────────

class ParticipantModelTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='user@test.com', password='pass')
        self.city = Cities.objects.create(name='София', district=DistrictChoice.SOFIA)

    def test_str_full_name(self):
        p = Participant.objects.create(
            first_name='Иван', last_name='Иванов',
            contact_email='ivan@test.com', user=self.user
        )
        self.assertEqual(str(p), 'Иван Иванов')

    def test_str_strips_whitespace(self):
        p = Participant.objects.create(
            first_name='', last_name='',
            contact_email='anon@test.com', user=self.user
        )
        self.assertEqual(str(p), '')

    def test_participant_linked_to_user(self):
        p = Participant.objects.create(
            first_name='Test', last_name='User',
            contact_email='t@test.com', user=self.user
        )
        self.assertEqual(p.user, self.user)


class ParticipantEventRoleModelTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='user@test.com', password='pass')
        self.location = Location.objects.create(
            name='Loc', address='Addr', district=DistrictChoice.SOFIA, user=self.user
        )
        self.event = Event.objects.create(
            title='Test Event', date=datetime.date.today(),
            location=self.location, description='Desc'
        )
        self.role = Role.objects.create(name='TestRole')
        self.participant = Participant.objects.create(
            first_name='Анна', last_name='Петрова',
            contact_email='anna@test.com', user=self.user
        )
        self.per = ParticipantEventRole.objects.create(
            participant=self.participant, event=self.event, role=self.role
        )

    def test_str_contains_name(self):
        self.assertIn('Анна', str(self.per))

    def test_str_contains_role(self):
        self.assertIn('TestRole', str(self.per))

    def test_unique_constraint_raises_on_duplicate(self):
        with self.assertRaises(Exception):
            ParticipantEventRole.objects.create(
                participant=self.participant, event=self.event, role=self.role
            )

    def test_same_participant_different_role_allowed(self):
        role2 = Role.objects.create(name='Role2')
        per2 = ParticipantEventRole.objects.create(
            participant=self.participant, event=self.event, role=role2
        )
        self.assertIsNotNone(per2.pk)


# ─── Views ────────────────────────────────────────────────────────────────────

class ParticipantListViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='user@test.com', password='pass')

    def test_list_requires_login(self):
        response = self.client.get(reverse('participant_list'))
        self.assertEqual(response.status_code, 302)

    def test_list_accessible_when_logged_in(self):
        self.client.login(email='user@test.com', password='pass')
        response = self.client.get(reverse('participant_list'))
        self.assertEqual(response.status_code, 200)


class ParticipantCreateViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='user@test.com', password='pass')

    def test_create_requires_login(self):
        response = self.client.get(reverse('participant_create'))
        self.assertEqual(response.status_code, 302)

    def test_create_participant_form_valid(self):
        self.client.login(email='user@test.com', password='pass')
        self.client.post(reverse('participant_create'), {
            'first_name': 'Test',
            'last_name': 'User',
            'contact_email': 'testuser@test.com',
        })
        self.assertTrue(Participant.objects.filter(
            first_name='Test', user=self.user
        ).exists())

    def test_created_participant_linked_to_logged_in_user(self):
        self.client.login(email='user@test.com', password='pass')
        self.client.post(reverse('participant_create'), {
            'first_name': 'Linked',
            'last_name': 'User',
            'contact_email': 'linked@test.com',
        })
        p = Participant.objects.get(first_name='Linked')
        self.assertEqual(p.user, self.user)


class ParticipantUpdateViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='user@test.com', password='pass')
        self.other = UserModel.objects.create_user(email='other@test.com', password='pass')
        self.participant = Participant.objects.create(
            first_name='Old', last_name='Name',
            contact_email='old@test.com', user=self.user
        )

    def test_update_own_participant(self):
        self.client.login(email='user@test.com', password='pass')
        self.client.post(reverse('participant_edit', args=[self.participant.pk]), {
            'first_name': 'New',
            'last_name': 'Name',
            'contact_email': 'new@test.com',
        })
        self.participant.refresh_from_db()
        self.assertEqual(self.participant.first_name, 'New')

    def test_cannot_update_other_users_participant(self):
        self.client.login(email='other@test.com', password='pass')
        response = self.client.get(reverse('participant_edit', args=[self.participant.pk]))
        self.assertEqual(response.status_code, 404)


class ParticipantDeleteViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='user@test.com', password='pass')
        self.participant = Participant.objects.create(
            first_name='Del', last_name='Me',
            contact_email='del@test.com', user=self.user
        )

    def test_delete_own_participant(self):
        self.client.login(email='user@test.com', password='pass')
        self.client.post(reverse('participant_delete', args=[self.participant.pk]))
        self.assertFalse(Participant.objects.filter(pk=self.participant.pk).exists())
