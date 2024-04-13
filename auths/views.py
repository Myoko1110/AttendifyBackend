import datetime
import secrets

import requests
from django.http import HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden, JsonResponse
from django.utils import timezone
from rest_framework.views import APIView

from main import settings
from auths.models import Session


class LoginView(APIView):
    def post(self, request):
        if "code" not in request.data:
            return HttpResponseBadRequest("Invalid request")

        code = request.data["code"]

        params = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URL,
            "grant_type": 'authorization_code',
        }

        token_res = requests.post("https://accounts.google.com/o/oauth2/token", data=params)
        if 400 < token_res.status_code < 599:
            return HttpResponseServerError("Internal Server Error")

        token_res_data = token_res.json()
        if "error" in token_res_data:
            if token_res_data["error"] == "invalid_request":
                return HttpResponseServerError(token_res_data["error"])

        print(token_res_data)

        access_token = token_res_data["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}
        userinfo_res = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers=headers)
        if 400 < token_res.status_code < 599:
            return HttpResponseServerError("Internal Server Error")


        user = userinfo_res.json()
        if "error" in token_res_data:
            if token_res_data["error"] == "invalid_request":
                return HttpResponseBadRequest("Invalid request")
            else:
                return HttpResponseServerError(token_res_data["error"])

        if "hd" not in user or user["hd"] != "toko.ed.jp":
            return HttpResponseForbidden("Forbidden")

        token = secrets.token_urlsafe(32)

        access_type = "normal"
        if user["email"] in settings.ALLOWED_USER:
            access_type = "executive"

        now = timezone.now().replace(microsecond=0)
        Session.objects.create(user_id=str(user["id"]), email=user["email"], token=token, access_type=access_type, created_at=now)

        res = {
            "status": 200,
            "user": user,
            "token": token,
            "type": access_type,
        }

        return JsonResponse(res, json_dumps_params={'ensure_ascii': False})


class SessionView(APIView):
    def get(self, request):
        if "token" not in request.query_params:
            return HttpResponseBadRequest("Invalid request")

        token = request.query_params["token"]

        if "userId" not in request.query_params:
            return HttpResponseBadRequest("Invalid request")

        user_id = request.query_params["userId"]

        is_valid = is_valid_token(user_id, token)
        if is_valid:
            return JsonResponse({
                "status": 200,
                "session": True,
                "type": is_valid,
            }, json_dumps_params={'ensure_ascii': False})

        else:
            return JsonResponse({
                "status": 200,
                "session": False,
            }, json_dumps_params={'ensure_ascii': False})


def is_valid_token(user_id, token):
    try:
        session = Session.objects.get(user_id=str(user_id), token=token)
    except Session.DoesNotExist:
        return False

    if session:
        expires_at = session.created_at + datetime.timedelta(minutes=settings.SESSION_MAX_AGE)
        if expires_at < timezone.now():
            return False

        return session.access_type

    else:
        return False
