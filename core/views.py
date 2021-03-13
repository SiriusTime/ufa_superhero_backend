from django.db.models import Count
from django.http import JsonResponse
from rest_framework import viewsets

from . import serializers
from . import models


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
