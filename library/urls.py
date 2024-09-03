from django.urls import path
from . import views

urlpatterns = [
  path('library/view/', views.library_books_list, name='library'),
  path('library/add-book/', views.add_book_to_library, name='library_add_book'),
  path('library/change-book/', views.update_library_book, name='library_change_book'),
  path('library/delete-book/', views.delete_library_book, name='delete_library_book')
]