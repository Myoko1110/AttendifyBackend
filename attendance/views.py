from datetime import datetime

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from rest_framework.views import APIView

from attendance.models import Attendance, Response
from auths.views import is_valid_token
from member.models import Member


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
        date = datetime.fromtimestamp(request.data["date"]).date()

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

        return HttpResponse(status=201)

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

        attendances = Attendance.objects.all().order_by("-date")
        return JsonResponse({
            "status": 200,
            "attendances": [
                {
                    "id": i.attendance_id,
                    "userId": i.user_id,
                    "date": datetime.combine(i.date, datetime.min.time()).timestamp(),
                    "type": i.type,
                }
                for i in attendances
            ]
        })

    def delete(self, request):
        if "token" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        token = request.data["token"]
        if "userId" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        user_id = request.data["userId"]

        is_valid = is_valid_token(user_id, token)
        if not is_valid:
            return HttpResponseForbidden("Forbidden")

        if "id" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        id = request.data["id"]

        try:
            Attendance.objects.get(attendance_id=id).delete()
        except Attendance.DoesNotExist:
            return HttpResponseBadRequest("Invalid request")
        return HttpResponse(status=200)

    def put(self, request):
        if "token" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        token = request.data["token"]
        if "userId" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        user_id = request.data["userId"]

        is_valid = is_valid_token(user_id, token)
        if not is_valid:
            return HttpResponseForbidden("Forbidden")

        if "id" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        id = request.data["id"]

        if "type" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        type = request.data["type"]

        try:
            attendance = Attendance.objects.get(attendance_id=id)
        except Attendance.DoesNotExist:
            return HttpResponseBadRequest("Invalid request")

        attendance.type = type
        attendance.save()

        return HttpResponse(status=200)


class AttendanceMemberView(APIView):
    def get(self, request, id):
        if "token" not in request.query_params:
            return HttpResponseBadRequest("Invalid request")
        token = request.query_params["token"]
        if "userId" not in request.query_params:
            return HttpResponseBadRequest("Invalid request")
        user_id = request.query_params["userId"]

        is_valid = is_valid_token(user_id, token)
        if not is_valid:
            return HttpResponseForbidden("Forbidden")

        try:
            attendances = Attendance.objects.filter(user_id=id).order_by("-date")
        except Attendance.DoesNotExists:
            return HttpResponseBadRequest("Does Not Exist")

        return JsonResponse({
            "status": 200,
            "attendances": [
                {
                    "id": i.attendance_id,
                    "userId": i.user_id,
                    "date": datetime.combine(i.date, datetime.min.time()).timestamp(),
                    "type": i.type,
                }
                for i in attendances
            ]
        })


class AttendancePartView(APIView):
    def get(self, request, part):
        if "token" not in request.query_params:
            return HttpResponseBadRequest("Invalid request")
        token = request.query_params["token"]
        if "userId" not in request.query_params:
            return HttpResponseBadRequest("Invalid request")
        user_id = request.query_params["userId"]

        is_valid = is_valid_token(user_id, token)
        if not is_valid:
            return HttpResponseForbidden("Forbidden")

        members = Member.objects.filter(part=part)
        attendances = []
        try:
            for i in members:
                attendances += Attendance.objects.filter(user_id=i.id).order_by("-date")
        except Attendance.DoesNotExists:
            return HttpResponseBadRequest("Does Not Exist")

        return JsonResponse({
            "status": 200,
            "attendances": [
                {
                    "id": i.attendance_id,
                    "userId": i.user_id,
                    "date": datetime.combine(i.date, datetime.min.time()).timestamp(),
                    "type": i.type,
                }
                for i in attendances
            ]
        })


class AttendanceGradeView(APIView):
    def get(self, request, grade):
        if "token" not in request.query_params:
            return HttpResponseBadRequest("Invalid request")
        token = request.query_params["token"]
        if "userId" not in request.query_params:
            return HttpResponseBadRequest("Invalid request")
        user_id = request.query_params["userId"]

        is_valid = is_valid_token(user_id, token)
        if not is_valid:
            return HttpResponseForbidden("Forbidden")

        members = Member.objects.filter(grade=grade)
        attendances = []
        try:
            for i in members:
                attendances += Attendance.objects.filter(user_id=i.id).order_by("-date")
        except Attendance.DoesNotExists:
            return HttpResponseBadRequest("Does Not Exist")

        return JsonResponse({
            "status": 200,
            "attendances": [
                {
                    "id": i.attendance_id,
                    "userId": i.user_id,
                    "date": datetime.combine(i.date, datetime.min.time()).timestamp(),
                    "type": i.type,
                }
                for i in attendances
            ]
        })


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
