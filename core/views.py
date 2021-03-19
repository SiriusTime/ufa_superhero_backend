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
    queryset = models.UserProfile.objects.all()


class LoginViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.Project.objects.all()

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