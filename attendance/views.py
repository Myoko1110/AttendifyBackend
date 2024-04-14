from datetime import datetime

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from rest_framework.views import APIView

from attendance.models import Attendance
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
        print(date)

        if "attendances" not in request.data:
            return HttpResponseBadRequest("Invalid request")

        attendance = request.data["attendances"]
        for i, j in attendance.items():
            Attendance.objects.create(user_id=i, date=date, type=j)

        return HttpResponse("success")
