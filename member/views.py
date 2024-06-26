from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from rest_framework.views import APIView

from auths.views import is_valid_token
from member.models import Member


class MemberView(APIView):
    def post(self, request):
        if "token" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        token = request.data["token"]
        if "userId" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        user_id = request.data["userId"]

        is_valid = is_valid_token(user_id, token)
        if is_valid != "executive":
            return HttpResponseForbidden("Forbidden")

        if "lastName" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        last_name = request.data["lastName"]

        if "firstName" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        first_name = request.data["firstName"]

        if "part" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        part = request.data["part"]

        if "grade" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        grade = request.data["grade"]

        Member.objects.create(last_name=last_name, first_name=first_name, part=part, grade=grade)

        return HttpResponse(status=201)

    def get(self, request):
        if "token" not in request.query_params:
            return HttpResponseBadRequest("Invalid request")
        token = request.query_params["token"]
        if "userId" not in request.query_params:
            return HttpResponseBadRequest("Invalid request")
        user_id = request.query_params["userId"]

        is_valid = is_valid_token(user_id, token)
        if is_valid != "executive" or is_valid != "normal":
            return HttpResponseForbidden("Forbidden")

        if "id" in request.query_params:
            try:
                result = Member.objects.get(id=request.query_params["id"])
                return JsonResponse({
                    "status": 200,
                    "member": {
                        "id": result.id,
                        "firstName": result.first_name,
                        "lastName": result.last_name,
                        "part": result.part,
                        "grade": result.grade,
                    }
                }, json_dumps_params={'ensure_ascii': False})

            except Member.DoesNotExist:
                return HttpResponseBadRequest("Does Not Exist")
        elif "part" in request.query_params:
            try:
                if "grade" in request.query_params:
                    result = Member.objects.filter(
                        Q(grade__startswith=request.query_params["grade"]),
                        part=request.query_params["part"]).order_by("-grade", "last_name", "first_name")
                else:
                    result = Member.objects.filter(part=request.query_params["part"])

                return JsonResponse({
                    "status": 200,
                    "members": [
                        {
                            "id": i.id,
                            "firstName": i.first_name,
                            "lastName": i.last_name,
                            "part": i.part,
                            "grade": i.grade,
                        }
                        for i in result
                    ]
                }, json_dumps_params={'ensure_ascii': False})

            except Member.DoesNotExist:
                return HttpResponseBadRequest("Does Not Exist")
        else:
            result = Member.objects.all().order_by("part", "-grade", "last_name", "first_name")

            return JsonResponse({
                "status": 200,
                "members": [
                    {
                        "id": i.id,
                        "firstName": i.first_name,
                        "lastName": i.last_name,
                        "part": i.part,
                        "grade": i.grade,
                    }
                    for i in result
                ]
            }, json_dumps_params={'ensure_ascii': False})

    def delete(self, request):
        if "token" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        token = request.data["token"]
        if "userId" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        user_id = request.data["userId"]

        is_valid = is_valid_token(user_id, token)
        if is_valid != "executive":
            return HttpResponseForbidden("Forbidden")

        if "ids" not in request.data:
            return HttpResponseBadRequest("Invalid request")

        ids = request.data["ids"]
        for i in ids:
            try:
                Member.objects.get(id=i).delete()
            except Member.DoesNotExist:
                pass

        return HttpResponse(status=200)

    def put(self, request):
        if "token" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        token = request.data["token"]
        if "userId" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        user_id = request.data["userId"]

        is_valid = is_valid_token(user_id, token)
        if is_valid != "executive":
            return HttpResponseForbidden("Forbidden")

        if "id" not in request.data:
            return HttpResponseBadRequest("Invalid request")
        id = request.data["id"]

        try:
            m = Member.objects.get(pk=id)
        except Member.DoesNotExist:
            return HttpResponseBadRequest("Does Not Exist")

        if "lastName" in request.data:
            m.last_name = request.data["lastName"]

        if "firstName" in request.data:
            m.first_name = request.data["firstName"]

        if "part" in request.data:
            m.part = request.data["part"]

        if "grade" in request.data:
            m.grade = request.data["grade"]

        m.save()
        return HttpResponse(status=200)
