from django.db import transaction
from rest_framework import serializers
from . import models


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile

        fields = (
            'id', 'email', 'password', 'phone'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    @transaction.atomic()
    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.set_password()
        instance.generate_token()
        instance.generate_code()
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category

        fields = (
            'id', 'category',
        )

    @transaction.atomic()
    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.save()
        return instance


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project

        fields = (
            'id', 'name', 'email', 'inn', 'link', 'title', 'text', 'category'
        )

    @transaction.atomic()
    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.save()
        return instance