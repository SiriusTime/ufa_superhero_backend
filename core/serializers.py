from django.db import transaction
from rest_framework import serializers
from . import models, services


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile

        fields = (
            'id', 'email', 'password',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    @transaction.atomic()
    def create(self, validated_data):
        instance = super().create(validated_data)
        services.crypt(validated_data['password'])
        instance.save()
        return instance