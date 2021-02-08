from django.contrib import admin
from .models import *
# Register your models here.

'''
The Django admin application can use your models to automatically build a site area 
that you can use to create, view, update, and delete records. 
'''

'''
This is the simplest way of registering a model, or models, with the site. 
The admin site is highly customisable, 
and we'll talk more about the other ways of registering your models further down.
'''

# admin.site.register(Book)
# admin.site.register(BookInstance)
# admin.site.register(Author)
admin.site.register(Language)
admin.site.register(Genre)

# Inline Book -> Author
class BookInline(admin.TabularInline):
    model = Book
    extra = 0

# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['last_name','first_name','date_of_birth','date_of_death']

    # The fields attribute lists just those fields that are to be displayed on the form, in order.
    fields = ['first_name', 'last_name',('date_of_birth','date_of_death')]
    # exclude = []

    inlines = [BookInline]

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

# Inline BookInstance -> Book
class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Unfortunately we can't directly specify the genre field in list_display because it is a ManyToManyField
    # (Django prevents this because there would be a large database access "cost" in doing so)
    list_display = ['title','author','display_genre']
    inlines = [BookInstanceInline]

# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstance(admin.ModelAdmin):
    list_display = ['id','book','status','due_back','borrower']

    list_filter = ['status','due_back','borrower']

    fieldsets = (
        ('Book info',{'fields':('id','book','imprint')}),
        ('Availability',{'fields':('status','due_back','borrower')})
    )
