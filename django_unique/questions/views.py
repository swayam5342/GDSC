from django.shortcuts import render, HttpResponse
# Create your views here.
def home (request):
    # return HttpResponse("This is the data")
    context = { 'name' : "john", "course":"beee"}
    return render(request, 'index.html',context)

def about (request):
    # return HttpResponse("This is the about")
    return render(request, 'about.html')

def questions (request):
    # return HttpResponse("This is the questions")
    return render(request, 'question1.html')

def signup (request):
    # return HttpResponse("This is the signup")
    return render(request, 'signup.html')