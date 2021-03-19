from django.http import JsonResponse
from rest_framework import viewsets

from . import serializers
from . import models
from . import services


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProjectSerializer
    queryset = models.Project.objects.all()

    def make_struct(self, data):
        return {
            'id': data.id,
            'name': data.name,
            'email': data.email,
            'inn': data.inn,
            'link': data.link,
            'title': data.title,
            'text': data.text,
            'category': data.category
        }

    def list(self, request, *args, **kwargs):
        try:
            instance = models.Project.objects.filter(category=request.query_params["category"])
            data = [self.make_struct(case) for case in instance]
            return JsonResponse({"data": data})
        except KeyError:
            return JsonResponse({"data": super().list(request)})


class LoginViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = models.UserProfile.objects.filter(email=request.data["email"])
            password = services.crypt(request.data['password'])
        except KeyError:
            return JsonResponse({
                "error": "data not found"
            })

        if user and user.password == password:
            return JsonResponse({
                "id": user.pk,
            })
        else:
            return JsonResponse({
                "error": "not user or password failed"
            })