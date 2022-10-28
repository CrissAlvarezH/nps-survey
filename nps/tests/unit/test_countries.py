from django.test import TransactionTestCase

from nps.services.countries import (
    country_get,
    country_list,
    country_exists
)
from nps.tests.factories import CountryFactory


class CountriesTestCase(TransactionTestCase):

    def test_country_insert_and_fetch(self):
        [_, country2, country3] = CountryFactory.create(amount=3)

        exists = country_exists(name=country2.name)
        self.assertTrue(exists)

        countries_in_db = country_list()
        self.assertEqual(countries_in_db.count(), 3)

        country3_in_db = country_get(name=country3.name)
        self.assertEqual(country3_in_db.name, country3.name)
