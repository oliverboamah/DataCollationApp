from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index.html', {})


def users(request):
    return render(request, 'users.html', {})


def upload_file(request):
    return render(request, 'upload_file.html', {})
