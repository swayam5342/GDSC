from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home or any page after successful login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

# Create your views here.
def home (request):
    # return HttpResponse("This is the data")
    context = { 'name' : "john", "course":"beee"}
    return render(request, 'index.html',context)

def about (request):
    # return HttpResponse("This is the about")
    return render(request, 'about.html')

def question1(request):
    return render(request, 'question1.html')

def question2(request):
    return render(request, 'question2.html')

def question3(request):
    return render(request, 'question3.html')

def question4(request):
    return render(request, 'question4.html')

def question5(request):
    return render(request, 'question5.html')

def question6(request):
    return render(request, 'question6.html')

def question7(request):
    return render(request, 'question7.html')

def question8(request):
    return render(request, 'question8.html')

def question9(request):
    return render(request, 'question9.html')

def question10(request):
    return render(request, 'question10.html')

def result(request):
    return render(request, 'result.html')


def profile(request):
    return render(request, 'profile.html')

def signup (request):
    # return HttpResponse("This is the signup")
    return render(request, 'signup.html')