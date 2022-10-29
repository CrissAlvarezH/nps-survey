from rest_framework import status
from nps.models import CompanyUser

from nps.tests.factories import UserFactory
from .setup import ApiBaseTest, SetupCompaniesData


class CompaniesApiTest(SetupCompaniesData, ApiBaseTest):
    def test_fetch_company(self):
        resp = self.client.get("/api/v1/nps/companies/")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get("pagination_data").get("count"), len(self.companies))

        resp = self.client.get(f"/api/v1/nps/companies/{self.companies[0].id}/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get("id"), self.companies[0].id)

    def test_create_company(self):
        body = {
            "name": "Company testing",
            "description": "desc company",
            "country_name": self.countries[0].name
        }
        resp = self.client.post(
            "/api/v1/nps/companies/",
            body,
            format="json"
        )

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data.get("name"), body.get("name"))

    def test_update_company(self):
        company = self.companies[0]
        company.name = company.name + " updated"

        body = {
            "name": company.name,
            "description": company.description,
            "country_name": company.country_name.name
        }
        resp = self.client.put(
            f"/api/v1/nps/companies/{company.id}/",
            body,
            format="json"
        )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get("name"), body.get("name"))

    def test_delete_company(self):
        company = self.companies[0]

        resp = self.client.delete(f"/api/v1/nps/companies/{company.id}/")

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        resp = self.client.get(f"/api/v1/nps/companies/{company.id}/")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_fetch_persons_on_company(self):
        company = self.companies[0]
        resp = self.client.get(f"/api/v1/nps/companies/{company.id}/persons/")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get("pagination_data").get("count"), 5)

    def test_add_person_to_company(self):
        user = UserFactory.create()
        company = self.companies[0]

        body = {
            "user": {"id": user.id},
            "role": CompanyUser.Roles.CONSULTANT
        }
        resp = self.client.post(
            f"/api/v1/nps/companies/{company.id}/persons/",
            body,
            format="json"
        )

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp = self.client.get(f"/api/v1/nps/companies/{company.id}/persons/")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get("pagination_data").get("count"), 6)

    def test_remove_person_to_company(self):
        company = self.companies[0]
        user = company.companyuser_set.first().user

        resp = self.client.delete(f"/api/v1/nps/companies/{company.id}/persons/{user.id}/")

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        resp = self.client.get(f"/api/v1/nps/companies/{company.id}/persons/")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get("pagination_data").get("count"), 4)

    def test_error_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION=None)
        resp = self.client.get("/api/v1/nps/companies/")

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
