from django.db.models import Model, CharField, IntegerField, FloatField


class Book(Model):
    title = CharField(max_length=200)
    glasgow_link = CharField(max_length=1000, unique=True)
    goodreads_link = CharField(max_length=1000, unique=True)
    year = IntegerField(blank=True, null=True)
    authors = CharField(max_length=200)
    rating = FloatField(blank=True, null=True)
    reviews = IntegerField()

    def __str__(self):
        return f'Title: {self.title}, average: {self.rating}, reviews: {self.reviews}'

