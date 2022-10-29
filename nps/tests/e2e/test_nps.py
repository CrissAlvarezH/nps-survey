import random

from rest_framework import status

from nps.models import Nps

from .setup import ApiBaseTest, SetupCompaniesData


class NpsApiTest(SetupCompaniesData, ApiBaseTest):
    def setUp(self) -> None:
        response = super().setUp()

        nps_survey = []
        for user in self.users:
            nps_survey.append(Nps(
                person=user,
                answer=random.randint(0, 10)
            ))
        self.nps_survey = Nps.objects.bulk_create(nps_survey)

        return response

    def test_fetch_nps_surveys(self):
        resp = self.client.get("/api/v1/nps/surveys/")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get("pagination_data").get("count"), len(self.nps_survey))

    def test_take_nps_survey(self):
        user = self.users[0]
        user.user.set_password("password")
        user.user.save()
        body = {
            "answer": 6,
            "company_id": user.company.id,
        }

        self.login(user.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        resp = self.client.post(
            "/api/v1/nps/surveys/",
            body, format="json"
        )

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # check if there are one survey more
        resp = self.client.get("/api/v1/nps/surveys/")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get("pagination_data").get("count"), len(self.nps_survey) + 1)
