from django.urls import path
from . import views


app_name = 'library'

urlpatterns = [
  path('view/', views.library_books_list, name='library'),
  path('add-book/', views.add_book_to_library, name='library_add_book'),
  path('change-book/', views.update_library_book, name='change_library_book'),
  path('delete-book/', views.delete_library_book, name='delete_library_book')
]