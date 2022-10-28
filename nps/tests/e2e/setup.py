from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class ApiBaseTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(full_name="root", email="root@email.com")
        self.user.set_password("password")
        self.user.save()

        login_resp = self.client.post(
            "/api/v1/users/auth/",
            {"email": self.user.email, "password": "password"},
            format="json"
        )

        self.assertEqual(login_resp.status_code, status.HTTP_200_OK)

        self.token = login_resp.data.get("access")
        self.auth_header = {"Authorization": f"Bearer {self.token}"}

        return super().setUp()
