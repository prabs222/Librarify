from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('register-librarian/', registerLibrarian, name='register-librarian'),
    path('register-user/', myregister, name='register-user'),
    
    # path('librarian-login', librarianLogin, name='librarian-login'),
    path('user-login/', mylogin, name='myLogin'),
    path("logout/", myLogout, name="myLogout"),

    path('add-book/',addBook, name='add-book'),
    path('update-book/<str:pk>/',updateBook, name='add-book'),
    path('delete-book/<str:pk>/',deleteBook, name='delete-book'),
    path('get-books/',getBooks, name='get-book'),
    path('get-available-books/',getAvailableBooks, name='get-available-books'),
    # path('borrow-available-books/',getAvailableBooks, name='get-available-books'),
    path('borrow-book/<str:pk>/',borrowBook, name='borrow-book'),
    path('return-book/<str:pk>/',returnBook, name='return-book'),

    
]
