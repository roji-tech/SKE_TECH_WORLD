from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import View

from main.forms import LibraryBookForm
from main import mydecorators
from .models import Library, LibraryBook


# @lecturer_required
# @permission_required('library.can_view_book', raise_exception=True)
def library_books_list(request):
  library_books = LibraryBook.objects.all()
  return render(request, 'library.html', {'librarybooks' : library_books})




# @mydecorators.teacher_is_authenticated
# @permission_required('library.can_add_book', raise_exception=True)
def add_book_to_library(request):
    if request.method == 'POST':
        form = LibraryBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('library')
    else:
        form = LibraryBookForm()
    return render(request, 'library.html', {'form': form})

@login_required
@permission_required('library.can_change_book', raise_exception=True)
def update_library_book(request, pk):
    book = get_object_or_404(LibraryBook, pk=pk)
    if request.method == "POST":
        form = LibraryBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('library:library_book_list')
        
    else:
        form = LibraryBookForm(instance=book)
    return render(request, 'index.html', {'form': form , 'book' : book})


@login_required
@permission_required('library.can_delete_book', raise_exception=True)
def delete_library_book(request, pk):
    book = get_object_or_404(LibraryBook, pk=pk)
    if request.method == 'POST':
        book.delete()
        return reverse_lazy('library:library_book_list')
    return render(request, 'library.html', {'book' : book})