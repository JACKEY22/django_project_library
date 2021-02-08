import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from catalog.forms import RenewBookForm
from catalog.models import Book, BookInstance, Author


def index(request):
   num_books = Book.objects.all().count()
   num_instances = BookInstance.objects.all().count()
   num_instances_available = BookInstance.objects.filter(status__exact='A').count()
   num_authors = Author.objects.count() # The 'all()' is implied by default.

   # session
   num_visits = request.session.get('num_visits', 1)
   request.session['num_visits'] = num_visits + 1

   context = {'num_books':num_books,
              'num_instances':num_instances,
              'num_instances_available':num_instances_available,
              'num_authors':num_authors,
              'num_visits':num_visits}

   # Render the HTML template index.html with the data in the context variable
   return render(request,'index.html', context=context)

class BookListView(ListView):
    model = Book
    template_name = 'catalog/book_list.html'
    # paginate_by = 10
    # templates_name = the generic views look for templates in /application_name/the_model_name_list.html
    # context_object_name = book_list or object_list (default)

    # queryset = Book.objects.filter(title__icontains='flower')[:5]
    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='war')[:5]

    '''
    # to pass additional context variables to the template
    def get_context_data(self, **kwargs):
        book_list_english = Book.objects.filter(language__name__exact='English')
        context = super().get_context_data(**kwargs)
        context['book_list_english'] = book_list_english
        return context
    '''

class BookDetailView(DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
class BookCreateView(CreateView):
    model = Book
    fields = '__all__'

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
class BookUpdateView(UpdateView):
    model = Book
    fields = '__all__'

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy('book_list')
    template_name = 'catalog/book_delete.html'


class MybookListView(LoginRequiredMixin,ListView):
    models = BookInstance
    template_name = 'catalog/mybook_list.html'

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__iexact='o').order_by('due_back')

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
class BorrowedBookListView(ListView):
    model = BookInstance
    template_name = 'catalog/borrowed_book_list.html'

    def get_queryset(self):
        return BookInstance.objects.filter(status__iexact='o').order_by('due_back')


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid(): # clean_renewal_date
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('books-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date':proposed_renewal_date})

    context = {'form':form,'book_instance':book_instance}

    return render(request, 'catalog/renew_book.html', context=context )


class AuthorListView(ListView):
    model = Author
    template_name = 'catalog/author_list.html'

    # paginate_by =
    # context_object_name =
    # queryset =
    # def get_queryset(self):
    # def get_context_data(self, **kwargs):


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'


# need form - specify fields
@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
class AuthorCreateView(CreateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']
    initial = {'date_of_death':'11/06/2020'}
    # template_name = author_form (default)
    # success_url = detail

# need form
@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
class  AuthorUpdateView(UpdateView):
    model = Author
    fields = '__all__'
    # template_name = author_form (default)
    # success_url = detail

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
class AuthorDeleteView(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    template_name = 'catalog/author_delete.html'