from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import View

from main.forms import LibraryBookForm
from .models import Library, LibraryBook


@login_required
@permission_required('library.can_view_book', raise_exception=True)
def library_books_list(request):
  libraryBooks = LibraryBook.objects.all()
  return render(request, 'library/index.html', {'librarybooks' : libraryBooks})



@login_required
@permission_required('library.can_add_book', raise_exception=True)
def add_book_to_library(request):
    if request.method == 'POST':
        form = LibraryBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('library:book_list')
    else:
        form = LibraryBookForm()
    return render(request, 'library/book_form.html', {'form': form})

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
        form = LibraryBookForm()
    return render(request, 'index.html', {'form': form , 'book' : book})

def delete_library_book(request, pk):
    book = get_object_or_404(LibraryBook, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('library:library_book_list')