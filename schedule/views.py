from datetime import datetime

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from rest_framework.views import APIView

from auths.views import is_valid_token
from member.models import Member
from schedule.models import Schedule


class ScheduleView(APIView):
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

        if "scheduleType" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        schedule_type = request.data["scheduleType"]

        Schedule.objects.create(date=date, schedule_type=schedule_type)

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

        result = Schedule.objects.all().order_by("date")

        return JsonResponse({
            "schedules": [
                {
                    "date": i.date.strftime("%Y-%m-%d"),
                    "scheduleType": i.schedule_type
                }
                for i in result
            ]
        }, json_dumps_params={'ensure_ascii': False})

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

        if "date" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        date = datetime.fromtimestamp(request.data["date"]).date()

        try:
            s = Schedule.objects.get(date=date)
        except Member.DoesNotExist:
            return HttpResponseBadRequest("Does Not Exist")

        if "scheduleType" in request.data:
            s.schedule_type = request.data["scheduleType"]
        s.save()

        return HttpResponse(status=200)

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

        if "date" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        date = datetime.fromtimestamp(request.data["date"]).date()

        try:
            s = Schedule.objects.get(date=date)
            s.delete()
        except Member.DoesNotExist:
            return HttpResponseBadRequest("Does Not Exist")

        return HttpResponse(status=200)
