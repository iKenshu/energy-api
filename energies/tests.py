from django.core.management import call_command
from django.test import TestCase

from rest_framework.test import APIClient, APITestCase


class EnergyAPITest(APITestCase):

    def setUp(self) -> None:
        call_command("loaddata", "data.json", verbosity=0)
        return super().setUp()

    def test_url_exist_without_params(self) -> None:
        response = self.client.get("/api/")
        self.assertEqual(response.status_code, 200)

    def test_api_response_with_daily_params(self) -> None:
        data = {
            "period": "daily",
            "date": "2022-10-12"
        }
        response = self.client.get("/api/", data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_api_response_with_weekly_params(self) -> None:
        data = {
            "period": "weekly",
            "date": "2022-10-12"
        }
        response = self.client.get("/api/", data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_api_response_with_monthly_params(self) -> None:
        data = {
            "period": "monthly",
            "date": "2022-10-12"
        }
        response = self.client.get("/api/", data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_api_response_with_incorrect_date_format(self) -> None:
        data = {
            "period": "daily",
            "date": "incorrect"
        }
        response = self.client.get("/api/", data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_api_response_with_incorrect_period(self) -> None:
        data = {
            "period": "incorrect",
            "date": "2022-10-12"
        }
        response = self.client.get("/api/", data, format="json")
        self.assertEqual(response.status_code, 400)

