from django.test import TransactionTestCase
from nps.models import Company, CompanyUser, Country, Nps
from nps.services.nps import get_detractors_top_by_country, get_edge_top_by_country, get_promoters_top_by_country, nps_create, nps_get_by_id, nps_list

from users.models import User


class NpsTestCase(TransactionTestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(full_name="Cristian", email="cristian@email.com")
        self.country = Country.objects.create(name="Country1")
        self.company = Company.objects.create(
            name="Company1",
            description="company 1",
            country_name=self.country
        )
        self.relationship = CompanyUser.objects.create(
            user=self.user,
            company=self.company,
            role=CompanyUser.Roles.ACCOUNT_MANAGER
        )
        return super().setUp()

    def test_nps_insert_and_fetch(self):
        nps = nps_create(user=self.user, company_id=self.company.id, answer=5)

        nps_in_db = nps_get_by_id(nps.id)
        self.assertEqual(nps.id, nps_in_db.id)
        self.assertEqual(nps.answer, nps_in_db.answer)

        all_nps_in_db = nps_list()
        self.assertEqual(all_nps_in_db.count(), 1)


class NpsReportsTestCase(TransactionTestCase):

    def setUp(self) -> None:
        self.users = [
            User.objects.create(full_name=name, email=email)
            for name, email in [
                ("User 1", "user1@email.com"),
                ("User 2", "user2@email.com"),
                ("User 3", "user3@email.com"),
                ("User 4", "user4@email.com"),
            ]
        ]
        self.countries = [
            Country.objects.create(name=name)
            for name in ["Country1", "Country2"]
        ]
        self.companies = [
            Company.objects.create(name=name, description=desc, country_name=country)
            for name, desc, country in [
                ("Company 1", "C1", self.countries[0]),
                ("Company 2", "C2", self.countries[1])
            ]
        ]

        # two users in each company
        self.company_user = [
            CompanyUser.objects.create(company=company, user=user)
            for company, user in [
                (self.companies[0], self.users[0]),
                (self.companies[0], self.users[1]),
                (self.companies[1], self.users[2]),
                (self.companies[1], self.users[3]),
            ]
        ]
        self.nps_survey = [
            Nps.objects.create(person=self.company_user[0], answer=4),  # detractor
            Nps.objects.create(person=self.company_user[1], answer=1),  # detractor
            Nps.objects.create(person=self.company_user[2], answer=9),  # promoter
            Nps.objects.create(person=self.company_user[3], answer=10),  # promoter
        ]

        # expected values
        self.country1_detractors_top_len = 2
        self.country2_detractors_top_len = 0
        self.country1_worse_detractor = self.company_user[1]

        self.country1_promoters_top_len = 0
        self.country2_promoters_top_len = 2
        self.country2_best_promoter = self.company_user[3]
        return super().setUp()

    def test_nps_detractors_top(self):
        country1_detractors = get_detractors_top_by_country(country=self.countries[0].name)
        self.assertEqual(len(country1_detractors), self.country1_detractors_top_len)
        self.assertEqual(country1_detractors[0], self.country1_worse_detractor)

        country2_detractors = get_detractors_top_by_country(country=self.countries[1].name)
        self.assertEqual(len(country2_detractors), self.country2_detractors_top_len)

    def test_nps_promoters_top(self):
        country1_promoters = get_promoters_top_by_country(country=self.countries[0].name)
        self.assertEqual(len(country1_promoters), self.country1_promoters_top_len)

        country2_promoters = get_promoters_top_by_country(country=self.countries[1].name)
        self.assertEqual(len(country2_promoters), self.country2_promoters_top_len)
        self.assertEqual(country2_promoters[0], self.country2_best_promoter)

    def test_nps_edge_top(self):
        c1_best_promoter, c1_worse_detractor = get_edge_top_by_country(
            country=self.countries[0].name)
        self.assertEqual(c1_best_promoter, None)
        self.assertEqual(c1_worse_detractor, self.country1_worse_detractor)

        c2_best_promoter, c2_worse_detractor = get_edge_top_by_country(
            country=self.countries[1].name)
        self.assertEqual(c2_best_promoter, self.country2_best_promoter)
        self.assertEqual(c2_worse_detractor, None)
