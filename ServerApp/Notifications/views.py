from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Notification
from django.views.decorators.http import require_http_methods
import json
from .helpers import Helpers
from ServerApp import utils


# Create your views here.
@require_http_methods(["GET", "POST"])
def all_notifications(request):
    if request.method == "GET":
        utils.func()
        notifications = list(Notification.objects.all().values())
        return Helpers.success_response(notifications)

    elif request.method == "POST":
        data = json.loads(request.body)
        notification = Notification.objects.create(title=data['title'], content=data['content'])
        return Helpers.success_created(notification.__str__())


@require_http_methods(["GET", "PUT", "DELETE"])
def notification_detail(request, pk):
    try:
        if request.method == "GET":
            print("Notification", pk)
            notification = get_object_or_404(Notification, pk=pk)
            return Helpers.success_response(notification.__str__())
        elif request.method == "PUT":
            return JsonResponse({"message": "Notification updated successfully"})
        elif request.method == "DELETE":
            return JsonResponse({"message": "Notification deleted successfully"})
    except Exception as e:
        return Helpers.internal_server_error(str(e))
