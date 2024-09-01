from django.db import models
from main.models.models import School
# Create your models here.


class Library(models.Model):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name='library')
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=20, unique=True)
    available_copies = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class LibraryBook(models.Model):
    library = models.ForeignKey(
        Library, on_delete=models.CASCADE, related_name="library")
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    isbn = models.CharField(max_length=20)
    available_copies = models.IntegerField()

    def __str__(self):
        return self.title