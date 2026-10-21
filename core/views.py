from django.shortcuts import render

# Create your views here.
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()

        return JsonResponse({
            "status": "ok",
            "database": "connected",
        })

    except Exception:
        # Do not expose database credentials or internal errors.
        return JsonResponse(
            {
                "status": "error",
                "database": "unavailable",
            },
            status=503,
        )