from datetime import date
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse

# we've created the Genre as a model
# rather than as free text or a selection list
# so that the possible values can be managed through the database rather than being hard coded.
class Genre(models.Model):
    # Model representing a book genre.
    name = models.CharField(max_length=100, help_text='Enter a book genre (e.g. Science Fiction')

    # String for representing the Model object.
    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=100, help_text='English, French, Korean..')

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True) # if author deleted

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')

    # first arg is verbose_name
    isbn = models.CharField('ISBN',max_length=13, unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select a genre fot this book')

    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        # String for representing the Model object.
        return self.title

    def get_absolute_url(self):
        # Returns the url to access a detail record for this book.
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
       return ', '.join(genre.name for genre in self.genre.all()[:2])


import uuid
class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this book')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=100)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('A','Available'),
        ('M','Maintenance'),
        ('O','On loan'),
        ('R','Reserved'),
    )

    status = models.CharField( # in template - get_status_display
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='M',
        help_text='Book availability',
    )

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['due_back']
        permissions = (('can_mark_returned','Set book as returned'),)

    def __str__(self):
        return f'{self.id} - {self.book}' # book.title?

    # @property
    def is_overdue(self):
        if self.due_back and date.today() < self.due_back:
            return False
        return True

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name} {self.first_name}'
