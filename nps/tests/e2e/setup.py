from typing import Optional
from rest_framework import status
from rest_framework.test import APITestCase

from nps.tests.factories import CompanyFactory, CountryFactory, UserFactory

from users.models import User


class ApiBaseTest(APITestCase):
    def setUp(self) -> None:
        self.login()
        return super().setUp()

    def login(self, user: Optional[User] = None):
        self.client.credentials(HTTP_AUTHORIZATION=None)

        if user is not None:
            self.auth_user = user
        else:
            self.auth_user = User.objects.create(full_name="root", email="root@email.com")
            self.auth_user.set_password("password")
            self.auth_user.save()

        login_resp = self.client.post(
            "/api/v1/users/auth/",
            {"email": self.auth_user.email, "password": "password"},
            format="json"
        )

        self.assertEqual(login_resp.status_code, status.HTTP_200_OK)

        self.token = login_resp.data.get("access")
        self.auth_header = {"Authorization": f"Bearer {self.token}"}


class SetupCompaniesData(ApiBaseTest):
    def setUp(self) -> None:
        self.countries = CountryFactory.create(amount=3)

        self.companies = []
        for country in self.countries:
            self.companies.extend(CompanyFactory.create(country=country, amount=10))

        self.users = []
        for company in self.companies:
            self.users.extend(UserFactory.create_company_relationship(company, amount=5))

        response = super().setUp()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        return response
