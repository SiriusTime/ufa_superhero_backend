from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework import viewsets

from . import serializers
from . import models


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            auth = request._request.META['HTTP_AUTHORIZATION']
            user = models.UserProfile.objects.get(authorization=auth)
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
            'category': data.category
        }

    def list(self, request, *args, **kwargs):
        try:
            instance = models.Project.objects.filter(category=request.query_params["category"])
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