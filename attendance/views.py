from datetime import datetime

from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from rest_framework.views import APIView

from attendance.models import Attendance, Response
from auths.views import is_valid_token


class AttendanceView(APIView):
    def post(self, request):
        if "token" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        token = request.data["token"]
        if "userId" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        user_id = request.data["userId"]

        is_valid = is_valid_token(user_id, token)
        if not is_valid:
            return HttpResponseForbidden("Forbidden")

        if "date" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        date = datetime.fromtimestamp(request.data["date"])

        if "part" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        part = request.data["part"]

        if "grade" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        grade = request.data["grade"]

        if "attendances" not in request.data:
            return HttpResponseBadRequest("Invalid request")

        attendance = request.data["attendances"]
        for i, j in attendance.items():
            Attendance.objects.update_or_create(user_id=i, date=date, defaults={"type": j})

        Response.objects.get_or_create(part=part, date=date, grade=grade)

        return JsonResponse({"status": 200})


class ResponseView(APIView):
    def get(self, request):
        if "token" not in request.query_params:
            return HttpResponseBadRequest("Invalid request")
        token = request.query_params["token"]
        if "userId" not in request.query_params:
            return HttpResponseBadRequest("Invalid request")
        user_id = request.query_params["userId"]

        is_valid = is_valid_token(user_id, token)
        if not is_valid:
            return HttpResponseForbidden("Forbidden")

        if "date" not in request.query_params:
            return HttpResponseBadRequest("Invalid request")
        date = datetime.fromtimestamp(int(request.query_params["date"])).date()

        if "grade" not in request.query_params:
            return HttpResponseBadRequest("Invalid request")
        grade = request.query_params["grade"]

        if "part" not in request.query_params:
            return HttpResponseBadRequest("Invalid request")
        part = request.query_params["part"]

        response = Response.objects.filter(part=part, date=date, grade=grade)
        return JsonResponse({"status": 200, "responseExists": bool(response)})
