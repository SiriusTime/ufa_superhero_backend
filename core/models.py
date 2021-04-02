import datetime
import hashlib
import random
import string
import uuid

from django.db import models


class UserProfile(models.Model):
    email = models.EmailField(max_length=32, unique=True)
    phone = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=132)
    authorization = models.TextField(null=True)
    code_auth = models.CharField(max_length=6, null=True)
    is_sms = models.BooleanField(default=False)
    is_email = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    check = models.DateTimeField(default=datetime.datetime.today())
    date_joined = models.DateTimeField(default=datetime.datetime.today())

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = "profile"

    def generate_token(self):
        result = str(uuid.uuid4())
        self.authorization = result[0:64]

    def set_password(self):
        self.password = hashlib.sha256(self.password.encode()).hexdigest()

    def generate_code(self, size=4, chars=string.digits):
        self.code_auth = ''.join(random.choice(chars) for _ in range(size))


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