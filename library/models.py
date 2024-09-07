from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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
    # library = models.ForeignKey(
    #     Library, on_delete=models.CASCADE, related_name="library")
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='books' )
    book_image_url = models.URLField()
    available_copies = models.IntegerField()


    class Meta:
        permissions = [
            ('can_add_books', 'Can add books'),
            ('can_view_books', 'Can view books'),
            ('can_change_books', 'Can change books'),
            ('can_delete_books', 'Can delete books'),
        ]

    def __str__(self):
        return self.title
