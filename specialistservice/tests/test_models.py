from django.test import TestCase

from specialistservice.models import City, Specialist, Specialty, User


class VerboseNamePluralModelTest(TestCase):

    def test_city_verbose_name_plural(self):
        verbose_name_plural = City._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'cities')

    def test_specialty_verbose_name_plural(self):
        verbose_name_plural = Specialty._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'specialties')


class GetAbsoluteUrlModelTest(TestCase):

    def setUpTestData(cls):
        pass

    def test_specialist_get_absolute_url(self):
        pass
