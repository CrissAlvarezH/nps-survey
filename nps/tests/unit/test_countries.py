from django.test import TransactionTestCase

from nps.services.countries import (
    country_create,
    country_get,
    country_list,
    country_exists
)


class CountriesTestCase(TransactionTestCase):

    def test_country_insert_and_fetch(self):
        country_create(name="Country1")
        country_create(name="Country2")
        country_create(name="Country3")

        exists = country_exists(name="Country2")
        self.assertTrue(exists)

        countries_in_db = country_list()
        self.assertEqual(countries_in_db.count(), 3)

        country3 = country_get(name="Country3")
        self.assertEqual(country3.name, "Country3")
