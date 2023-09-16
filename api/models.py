from django.db.models import Model
from rest_framework.fields import CharField


class Book(Model):
    glasgow_link = CharField()