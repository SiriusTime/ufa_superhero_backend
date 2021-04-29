import json

from django.db import IntegrityError
from django.http import JsonResponse
from django.views.generic.base import View
from rest_framework import viewsets

from . import serializers
from . import models


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            auth = request._request.META['HTTP_AUTHORIZATION']
            user = models.UserProfile.objects.filter(authorization=auth).first()
        except KeyError:
            user = None

        if user:
            response = JsonResponse({
                "id": user.pk,
                "email": user.email,
                "phone": user.phone,
                "first_name": user.first_name,
                "last_name": user.last_name
            })
            user.generate_token()
            user.save()
            response["authorization"] = user.authorization
        else:
            response = JsonResponse({"error": "user not found"})

        return response


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            return JsonResponse({"data": super().create(request)})
        except IntegrityError:
            return JsonResponse({"error": "a duplicate key value violates a unique constraint"})


class ProjectViewSet(viewsets.ModelViewSet):  # TODO add response for create
    serializer_class = serializers.ProjectSerializer
    queryset = models.Project.objects.all()

    def make_struct(self, data):
        return {
            'id': data.id,
            # 'user': data.user,
            'inn': data.inn,
            'link': data.link,
            'title': data.title,
            'text': data.text,
            'category': data.category,
            'type_project': data.type_project
        }

    def list(self, request, *args, **kwargs):
        try:
            instance = models.Project.objects.filter(name__icontains=request.query_params["category"])
            if instance:
                data = [self.make_struct(case) for case in instance]
            else:
                data = None
            return JsonResponse({"data": data})
        except KeyError:
            return super().list(request)


class LoginViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = models.UserProfile.objects.filter(email=request.data["email"]).first()
            if user:
                password = user.password
                user.password = request.data['password']
                user.set_password()
            else:
                return JsonResponse({
                    "error": "user not found"
                })
        except KeyError:
            return JsonResponse({
                "error": "data not found"
            })

        if user.password == password:
            response = JsonResponse({
                "id": user.pk,
                "email": user.email,
                "phone": user.phone,
                "first_name": user.first_name,
                "last_name": user.last_name
            })
            user.generate_token()
            user.save()
            response["authorization"] = user.authorization

            return response
        else:
            return JsonResponse({
                "error": "password failed"
            })


class Logout(View):

    def post(self, request, *args, **kwargs):
        try:
            auth = request.META['HTTP_AUTHORIZATION']
            user = models.UserProfile.objects.filter(authorization=auth).first()
        except KeyError:
            user = None

        if user:
            user.generate_token()
            user.save()

            return JsonResponse({
                "success": True
            })

        return JsonResponse({
            "success": False
        })


class ProjectFavoriteViewSet(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf8').replace("'", '"'))
        try:
            user = data["user"]
            proj = data["project"]
        except KeyError:
            return JsonResponse({
            "error": "KeyError"
        })

        if not models.Project.objects.filter(pk=proj):
            return JsonResponse({
            "error": "Project not found"
        })

        _favorite = models.FavoriteProj.objects.filter(user=user).first()
        _count = models.CountFavoriteProj.objects.filter(project=proj).first()

        if _favorite:
            _favorite.projects = _favorite.projects.append(proj)
            _favorite.save()

        else:
            data = {
                "user": user,
                "projects": [proj, ]
            }
            _favorite = models.FavoriteProj(data)
            _favorite.save()

        if _count:
            _count._count += 1
            _count.save()

        else:
            data = {
                "project": proj,
                "count": 1
            }
            _count = models.CountFavoriteProj(data)
            _count.save()

        return JsonResponse({
            "user": user,
            "project": proj,
            "count_for_user": len(_favorite.projects),
            "count_for_project": _count._count
        })