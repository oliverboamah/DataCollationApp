from django.shortcuts import render
from .tasks import upload_file_task
from django.contrib import messages
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from . import models


# Create your views here.
def index(request):
    return render(request, 'index.html', {'uploads': models.Upload.objects.all()})


def users(request, upload_id):
    return render(request, 'users.html', {
        'title': models.Upload.objects.filter(id=upload_id)[0].title,
        'users': models.User.objects.filter(upload_id=upload_id)
    })


def upload_file(request):
    return render(request, 'upload_file.html', {})


def upload(request):
    try:
        title = request.POST['title']
        file = request.FILES['myfile']

        if request.method == 'POST' and file:
            # save uploaded excel file to storage for processing
            my_file = file
            fs = FileSystemStorage()
            file_name = fs.save(my_file.name, my_file)

            # use background celery task for processing
            upload_file_task.delay(file_name, title)
            messages.success(request, 'File Upload is in progress! Wait a moment and refresh this page.')
            return redirect('index')

    except Exception as e:
        messages.error(request, 'File Upload failed!')
        return redirect('index')
