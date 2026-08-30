from django.contrib.staticfiles import finders
from django.test import Client, TestCase

from items.models import Item


class ApiTests(TestCase):
    def test_page_static_and_health(self):
        assert self.client.get("/").status_code == 200
        assert finders.find("styles.css") is not None
        response = self.client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["ok"] is True

    def test_items(self):
        created = self.client.post(
            "/api/items",
            data='{"name":"First item"}',
            content_type="application/json",
        )
        item_id = created.json()["item"]["id"]
        assert created.status_code == 201
        assert self.client.get("/api/items").json()["count"] == 1
        assert self.client.delete(f"/api/items/{item_id}").status_code == 200
        assert Item.objects.count() == 0

    def test_items_through_https_proxy(self):
        client = Client(enforce_csrf_checks=True)
        page = client.get(
            "/",
            HTTP_HOST="django-latuk993.amvera.io",
            HTTP_X_FORWARDED_PROTO="https",
        )
        token = page.cookies["csrftoken"].value
        created = client.post(
            "/api/items",
            data='{"name":"Proxy item"}',
            content_type="application/json",
            HTTP_HOST="django-latuk993.amvera.io",
            HTTP_ORIGIN="https://django-latuk993.amvera.io",
            HTTP_X_CSRFTOKEN=token,
            HTTP_X_FORWARDED_PROTO="https",
        )
        assert created.status_code == 201
