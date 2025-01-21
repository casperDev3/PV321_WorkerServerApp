from django.http import JsonResponse
import json


class Helpers:
    @staticmethod
    def success_response(data, status=200, warnings=None, meta=None):
        return JsonResponse({
            "data": data,
            "meta": {},
            "warnings": warnings,
            "success": True
        }, status=status)

    @staticmethod
    def success_created(data, status=201):
        return JsonResponse({
            "data": data,
            "meta": {},
            "success": True
        }, status=status)

    @staticmethod
    def internal_server_error(error, status=500):
        return JsonResponse({
            "data": None,
            "meta": {},
            "success": False,
            "error": error
        }, status=status)
