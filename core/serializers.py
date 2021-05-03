from django.db import transaction
from rest_framework import serializers
from . import models


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile

        fields = (
            'id', 'email', 'password', 'phone', 'first_name', 'last_name'
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
            'id', 'category', 'image'
        )

    @transaction.atomic()
    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.save()
        return instance


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag

        fields = ("id", "title")

    @transaction.atomic()
    def create(self, validated_data):
        validated_data["title"] = validated_data["title"].lower()
        instance = models.Tag(**validated_data)
        instance.save()
        return instance


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project

        fields = (
            'id', 'user', 'link', 'title', 'text', 'category', 'type_project'
        )

    @transaction.atomic()
    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.save()
        return instance


class UrDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UrData
        fields = '__all__'

    @transaction.atomic()
    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.save()