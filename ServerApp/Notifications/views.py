from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Notification
from django.views.decorators.http import require_http_methods
import json


# Create your views here.
@require_http_methods(["GET", "POST"])
def all_notifications(request):
    if request.method == "GET":
        notifications = Notification.objects.all()
        return JsonResponse({
            "data": list(notifications.values()),
            "success": True,
            "meta": {
                "total": len(notifications)
            },
        }, status=200)
    elif request.method == "POST":
        data = json.loads(request.body)
        notification = Notification.objects.create(title=data['title'], content=data['content'])
        return JsonResponse({
            "data": notification.__str__(),
            "meta": {},
            "success": True
        }, status=201)


@require_http_methods(["GET", "PUT", "DELETE"])
def notification_detail(request, pk):
    try:
        if request.method == "GET":
            print("Notification", pk)
            notification = get_object_or_404(Notification, pk=pk)
            return JsonResponse({
                "data": notification.__str__(),
                "meta": {},
                "success": True
            }, status=200)
        elif request.method == "PUT":
            return JsonResponse({"message": "Notification updated successfully"})
        elif request.method == "DELETE":
            return JsonResponse({"message": "Notification deleted successfully"})
    except Exception as e:
        return JsonResponse({"data": None, "meta": {}, "success": True, "error": e}, status=500)
