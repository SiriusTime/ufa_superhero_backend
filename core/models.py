from django.db import models


class UserProfile(models.Model):
    email = models.EmailField(max_length=32, unique=True)
    password = models.CharField(max_length=132)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = "profile"


class Category(models.Model):
    category = models.CharField(max_length=256)

    def __str__(self):
        return str(self.category)

    class Meta:
        db_table = "category"


class Project(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=64)
    inn = models.CharField(max_length=32)
    link = models.TextField()
    title = models.CharField(max_length=64)
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = "project"