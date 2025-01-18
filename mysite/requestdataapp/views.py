from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import UserBioForm, FileUploadForm


# Create your views here.

def proces_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get('a', '')
    b = request.GET.get('b', '')
    res = a + b
    context = {
        'a': a,
        'b': b,
        'res': res,
    }
    return render(request,
      'requestdataapp/request-query-params.html', context=context)

def user_form(request:HttpRequest) -> HttpResponse:
    context = {
        'form': UserBioForm()
    }
    return render(request, 'requestdataapp/user-bio-form-djangoforms.html',
                  context=context)

def handle_file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            #myfile = request.FILES['myfile']
            myfile = form.cleaned_data['file']
            fs = FileSystemStorage()
            fail_name = fs.save(myfile.name, myfile)
            print(f'saved file {fail_name} ')
    else:
        form = FileUploadForm()
    context = {
        'form': form
    }
    return render(request, 'requestdataapp/file-upload.html',
                  context=context)


MAX_FILE_SIZE = 1024 * 1024


def handle_file_limit_upload(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST' and request.FILES.get('myfile'):
        myfile = request.FILES['myfile']

        if myfile.size > MAX_FILE_SIZE:
            return render(request,
                          'requestdataapp/error-file.html',)

        fs = FileSystemStorage()
        file_name = fs.save(myfile.name, myfile)
        print(f'Saved file: {file_name}')
        context = {
            'message': f'Файл успешно загружен: {file_name}'
        }
        return render(request, 'requestdataapp/file-upload.html',
                      context=context)

    return render(request, 'requestdataapp/file-upload.html')


