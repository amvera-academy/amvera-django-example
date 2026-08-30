import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_http_methods

from items.models import Item


@ensure_csrf_cookie
def index(request):
    return render(request, "index.html")


@require_GET
def health(request):
    return JsonResponse(
        {
            "ok": True,
            "framework": "Django",
            "storage": str(settings.DATABASES["default"]["NAME"]),
        }
    )


@require_http_methods(["GET", "POST"])
def items(request):
    if request.method == "GET":
        values = list(Item.objects.order_by("-id").values("id", "name"))
        return JsonResponse({"items": values, "count": len(values)})

    data = json.loads(request.body or "{}")
    name = str(data.get("name", "")).strip()
    if not name or len(name) > 120:
        return JsonResponse({"error": "Name must contain from 1 to 120 characters"}, status=400)
    item = Item.objects.create(name=name)
    return JsonResponse({"item": {"id": item.id, "name": item.name}}, status=201)


@require_http_methods(["DELETE"])
def delete_item(request, item_id):
    deleted, _ = Item.objects.filter(id=item_id).delete()
    if deleted == 0:
        return JsonResponse({"error": "Item not found"}, status=404)
    return JsonResponse({"deleted": True, "id": item_id})
