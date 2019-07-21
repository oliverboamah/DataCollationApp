from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage


# Create your views here.
def index(request):
    return render(request, 'index.html', {})


def users(request):
    return render(request, 'users.html', {})


def upload_file(request):
    return render(request, 'upload_file.html', {})


def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'upload_file.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'upload_file.html')
