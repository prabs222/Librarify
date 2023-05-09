from django.shortcuts import render
from .models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.http import JsonResponse

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .serializers import *
# Create your views here.

def myregister(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        
        user_obj = User.objects.filter(username=username)
        if user_obj.exists():
            return JsonResponse("Username already exists",safe = False)
        user_obj = User.objects.filter(email=email)
        if user_obj.exists():
            return JsonResponse("Email already exists",safe = False)
        if password != cpassword:
            return JsonResponse("Passwords do not match",safe = False)
        user_obj = User(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()
        return JsonResponse("Account created",safe = False)
    else:
        return render(request,'register.html')

@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def registerLibrarian(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        
        user_obj = User.objects.filter(username=username)
        if user_obj.exists():
            return JsonResponse("Username already exists",safe = False)
        user_obj = User.objects.filter(email=email)
        if user_obj.exists():
            return JsonResponse("Email already exists",safe = False)
        if password != cpassword:
            return JsonResponse("Passwords do not match",safe = False)
        user_obj = User(username=username, email=email,is_librarian = True)
        user_obj.set_password(password)
        user_obj.save()
        return JsonResponse("Account created",safe = False)
    else:
        return render(request,'register.html')

@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def mylogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user_obj = User.objects.filter(username=username)
        if not user_obj.exists():
            return JsonResponse("Username doesnot exists",safe = False)
        user_obj = authenticate(username=username, password=password)
        if not user_obj:
            return JsonResponse("invalid credentials",safe = False)
        login(request, user_obj)
        print("Login successful")
        return JsonResponse("Login Succesfully",safe = False)
    else:
        return render(request,'login.html')


@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def myLogout(request):
    logout(request)
    return Response("Logged out successful")

@api_view(['POST'])
def addBook(request):
    if request.user.is_authenticated and request.user.is_librarian:
        serializer = BookSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    else:
        return Response("You are not allowed here", status=status.HTTP_400_BAD_REQUEST)
            

@api_view(['POST'])
def updateBook(request,pk):
    if request.user.is_authenticated and request.user.is_librarian:
        book = Book.objects.get(id=pk)
        serializer = BookSerializer(instance=book, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    else:
        return Response("You are not allowed here", status=status.HTTP_400_BAD_REQUEST)

            

@api_view(['DELETE'])
def deleteBook(request,pk):
    if request.user.is_authenticated and request.user.is_librarian:
        book = Book.objects.get(id=pk)
        book.delete()
        return Response("book deleted")
    else:
        return Response("You are not allowed here", status=status.HTTP_400_BAD_REQUEST)
                    
@api_view(['GET'])
def getBooks(request):
    if request.user.is_authenticated and request.user.is_librarian:
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        
        return Response(serializer.data)
    else:
        return Response("You are not allowed here", status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getAvailableBooks(request):
    if request.user.is_authenticated:
        if not request.user.has_borrowed:
            books = Book.objects.filter(is_available=True)
            serializer = BookSerializer(books, many=True)
            
            return Response(serializer.data)
        else:
            return Response("You have already borrower a book")
    else:
        return Response("You are not allowed here", status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def borrowBook(request,pk):
    if request.user.is_authenticated:
        if not request.user.has_borrowed:

            book = Book.objects.get(id=pk)
            request.data["is_available"] = False
            user = User.objects.get(username=request.user)
            
            serializer = BookSerializer(instance=book, data=request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                user = User.objects.get(username=request.user)
                user.save()
                return Response("Book borrowed successfully")
        else:
            return Response("You have already borrower a book")

    else:
        return Response("You are not allowed here", status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def returnBook(request,pk):
    if request.user.is_authenticated:
        book = Book.objects.get(id=pk)
        request.data["is_available"] = True
        
        serializer = BookSerializer(instance=book, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.user)
            user.save()
            return Response("Book returned")

        else:
            return Response("You have already borrower a book")

    else:
        return Response("You are not allowed here", status=status.HTTP_400_BAD_REQUEST)

