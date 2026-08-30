from django.urls import path

from items import views


urlpatterns = [
    path("", views.index),
    path("api/health", views.health),
    path("api/items", views.items),
    path("api/items/<int:item_id>", views.delete_item),
]
