from django.db import models


class UserProfile(models.Model):
    email = models.EmailField(max_length=32, unique=True)
    password = models.CharField(max_length=132)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = "profile"
