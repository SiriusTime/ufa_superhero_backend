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
    authorization = models.CharField(max_length=64, unique=True)
    code_auth = models.CharField(max_length=6, null=True)
    is_sms = models.BooleanField(default=False)
    is_email = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    check = models.DateTimeField(default=datetime.datetime.today())
    date_joined = models.DateTimeField(default=datetime.datetime.today())
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

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
    image = models.TextField()

    def __str__(self):
        return str(self.category)

    class Meta:
        db_table = "category"


class Tag(models.Model):
    title = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = "tag"


class Project(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    link = models.TextField()
    title = models.CharField(max_length=64)
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type_project = models.CharField(max_length=64)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = "project"