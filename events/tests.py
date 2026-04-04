import datetime
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from events.models import Event, Location, Role
from participants.choises import DistrictChoice

UserModel = get_user_model()


def make_user(email='user@test.com', password='pass1234!'):
    return UserModel.objects.create_user(email=email, password=password)


def make_location(user, name='Витоша', district=DistrictChoice.SOFIA):
    return Location.objects.create(name=name, address='Test Address', district=district, user=user)


def make_event(location, title='Test Event', days_offset=0):
    return Event.objects.create(
        title=title,
        date=datetime.date.today() + datetime.timedelta(days=days_offset),
        location=location,
        description='Test description',
    )


class LocationModelTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.location = make_location(self.user)

    def test_str(self):
        self.assertEqual(str(self.location), 'Витоша')

    def test_location_belongs_to_user(self):
        self.assertEqual(self.location.user, self.user)


class EventModelTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.location = make_location(self.user)
        self.event = make_event(self.location)

    def test_str_contains_title(self):
        self.assertIn('Test Event', str(self.event))

    def test_str_contains_date(self):
        self.assertIn(str(datetime.date.today()), str(self.event))


class RoleModelTest(TestCase):
    def test_str(self):
        role = Role.objects.create(name='Доброволец', description='Участва с труд')
        self.assertEqual(str(role), 'Доброволец')

    def test_role_name_unique(self):
        Role.objects.create(name='UniqueRole')
        with self.assertRaises(Exception):
            Role.objects.create(name='UniqueRole')


class EventListViewTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.location = make_location(self.user)
        self.event = make_event(self.location, title='Почистване на гора')

    def test_list_accessible_without_login(self):
        response = self.client.get(reverse('event_list'))
        self.assertEqual(response.status_code, 200)

    def test_list_shows_event(self):
        response = self.client.get(reverse('event_list'))
        self.assertContains(response, 'Почистване на гора')

    def test_filter_by_search_match(self):
        response = self.client.get(reverse('event_list') + '?search=Почистване')
        self.assertContains(response, 'Почистване на гора')

    def test_filter_by_search_no_match(self):
        response = self.client.get(reverse('event_list') + '?search=ZZZNOMATCH')
        self.assertNotContains(response, 'Почистване на гора')

    def test_filter_by_district(self):
        response = self.client.get(reverse('event_list') + '?district=SOFIA')
        self.assertContains(response, 'Почистване на гора')

    def test_sort_date_asc(self):
        response = self.client.get(reverse('event_list') + '?sort=date_asc')
        self.assertEqual(response.status_code, 200)

    def test_sort_date_desc(self):
        response = self.client.get(reverse('event_list') + '?sort=date_desc')
        self.assertEqual(response.status_code, 200)


class EventDetailViewTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.location = make_location(self.user)
        self.event = make_event(self.location, title='Detail Event')

    def test_detail_requires_login(self):
        response = self.client.get(reverse('event_detail', args=[self.event.pk]))
        self.assertEqual(response.status_code, 302)

    def test_detail_accessible_when_logged_in(self):
        self.client.login(email='user@test.com', password='pass1234!')
        response = self.client.get(reverse('event_detail', args=[self.event.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Detail Event')

    def test_detail_404_for_nonexistent(self):
        self.client.login(email='user@test.com', password='pass1234!')
        response = self.client.get(reverse('event_detail', args=[99999]))
        self.assertEqual(response.status_code, 404)


class EventCreateViewTest(TestCase):
    def setUp(self):
        self.user = make_user()
        perm = Permission.objects.get(codename='add_event')
        self.user.user_permissions.add(perm)
        self.location = make_location(self.user)

    def test_create_requires_login(self):
        response = self.client.get(reverse('event_create'))
        self.assertEqual(response.status_code, 302)

    def test_create_requires_permission(self):
        plain = UserModel.objects.create_user(email='plain@test.com', password='pass1234!')
        self.client.login(email='plain@test.com', password='pass1234!')
        response = self.client.get(reverse('event_create'))
        self.assertEqual(response.status_code, 403)

    def test_create_with_permission_saves_event(self):
        self.client.login(email='user@test.com', password='pass1234!')
        self.client.post(reverse('event_create'), {
            'title': 'New Event',
            'date': datetime.date.today(),
            'location': self.location.pk,
            'description': 'Some description',
        })
        self.assertTrue(Event.objects.filter(title='New Event').exists())


class EventDeleteViewTest(TestCase):
    def setUp(self):
        self.user = make_user()
        for codename in ['add_event', 'delete_event']:
            perm = Permission.objects.get(codename=codename)
            self.user.user_permissions.add(perm)
        self.location = make_location(self.user)
        self.event = make_event(self.location, title='To Delete')

    def test_delete_removes_event(self):
        self.client.login(email='user@test.com', password='pass1234!')
        self.client.post(reverse('event_delete', args=[self.event.pk]))
        self.assertFalse(Event.objects.filter(pk=self.event.pk).exists())
