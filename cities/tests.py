from django.test import TestCase
from cities.models import Cities
from participants.choises import DistrictChoice


class CitiesModelTest(TestCase):
    def test_str_format(self):
        city = Cities.objects.create(name='Пловдив', district=DistrictChoice.PLOVDIV)
        self.assertEqual(str(city), 'Пловдив , PLOVDIV')

    def test_unique_name_raises(self):
        Cities.objects.create(name='Варна', district=DistrictChoice.VARNA)
        with self.assertRaises(Exception):
            Cities.objects.create(name='Варна', district=DistrictChoice.BURGAS)

    def test_create_city(self):
        city = Cities.objects.create(name='Русе', district=DistrictChoice.RUSE)
        self.assertEqual(city.name, 'Русе')
        self.assertEqual(city.district, DistrictChoice.RUSE)
