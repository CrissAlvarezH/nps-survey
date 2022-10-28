from rest_framework.test import APITestCase

from users.models import User


class ApiBaseTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(full_name="root", email="root@email.com")
        self.user.set_password("password")

        login_resp = self.client(
            "/api/v1/users/auth",
            {"email": self.user.email, "password": "password"},
            format="json"
        )

        self.token = login_resp.data.get("access")

        return super().setUp()
