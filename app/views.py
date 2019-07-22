from django.shortcuts import render
from .tasks import upload_file_task
from django.contrib import messages
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from . import models


# loads homepage template
def index(request):
    return render(request, 'index.html', {'uploads': models.Upload.objects.all().order_by('-id')})


# loads users template(individual entries)
def users(request, upload_id):
    return render(request, 'users.html', {
        'title': models.Upload.objects.filter(id=upload_id)[0].title,
        'created_at': models.Upload.objects.filter(id=upload_id)[0].created_at,
        'users': models.User.objects.filter(upload_id=upload_id)
    })


# saves excel file to storage
# starts a celery background delay task to process uploaded excel file
def upload(request):
    try:
        title = request.POST['title']
        file = request.FILES['myfile']

        if request.method == 'POST' and file:

            # save uploaded excel file to storage for processing
            my_file = file
            fs = FileSystemStorage()
            file_name = fs.save(my_file.name, my_file)

            # use background celery task for processing the uploaded file
            upload_file_task.delay(file_name, title)

            # print background task progress to console
            messages.success(request, 'File Upload is in progress! Wait a moment and refresh this page.')

            # go back to the homepage
            return redirect('index')

    except Exception as e:

        # In case of errors, print an error message to console
        messages.error(request, 'File Upload failed!')

        # go back to homepage
        return redirect('index')
