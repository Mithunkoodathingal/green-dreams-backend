from django.shortcuts import render

# Create your views here.
import json
import time

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST


from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# Match the existing frontend's session contract.
ROLE_LABELS = {
    "SA": "Super Admin",
    "M": "Manager",
    "A": "Collection Agent",
    "P": "Panchayath User",
}


def serialize_user(user):
    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "role": user.role,
        "isActive": user.is_active,
    }


@require_GET
@ensure_csrf_cookie
def csrf_token(request):
    return JsonResponse({"detail": "CSRF cookie initialized."})





def session_payload(user, request):
    expiry_date = request.session.get_expiry_date()

    return {
        "id": str(user.id),
        "name": user.get_full_name() or user.email or user.username,
        "role": ROLE_LABELS.get(user.role, "Collection Agent"),
        "expiresAt": int(expiry_date.timestamp() * 1000),
    }

    # Add these IDs when the corresponding assignment models exist.
    # Do not invent agent or Panchayath IDs.
    return payload


@require_GET
@ensure_csrf_cookie
def csrf_token(request):
    return JsonResponse({"detail": "CSRF cookie initialized."})


@require_POST
def login_view(request):
    try:
        data = json.loads(request.body or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"detail": "Invalid JSON request."},
            status=400,
        )

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return JsonResponse(
            {"detail": "Email and password are required."},
            status=400,
        )

    # Email must identify exactly one account.
    matching_users = User.objects.filter(email__iexact=email)
    if matching_users.count() != 1:
        return JsonResponse(
            {"detail": "Invalid email or password."},
            status=401,
        )

    user_record = matching_users.first()
    user = authenticate(
        request,
        username=user_record.username,
        password=password,
    )

    if user is None or not user.is_active:
        return JsonResponse(
            {"detail": "Invalid email or password."},
            status=401,
        )

    login(request, user)
    request.session.set_expiry(timedelta(hours=1))

    return JsonResponse(session_payload(user, request))


@require_POST
def logout_view(request):
    logout(request)
    return JsonResponse({"detail": "Logged out successfully."})


@require_GET
def me_view(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"detail": "Authentication required."},
            status=401,
        )
        
    return JsonResponse(session_payload(request.user, request))
