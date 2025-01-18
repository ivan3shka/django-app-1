from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

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
    return render(request, 'requestdataapp/user-bio-form.html')

def handle_file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST' and request.FILES.get('myfile'):
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        fail_name = fs.save(myfile.name, myfile)
        print(f'saved file {fail_name} ')

    return render(request, 'requestdataapp/file-uploadd.html')


MAX_FILE_SIZE = 1024 * 1024


def handle_file_limit_upload(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST' and request.FILES.get('myfile'):
        myfile = request.FILES['myfile']

        if myfile.size > MAX_FILE_SIZE:
            return render(request,
                          'requestdataapp/upload-limit.html',)

        fs = FileSystemStorage()
        file_name = fs.save(myfile.name, myfile)
        print(f'Saved file: {file_name}')
        context = {
            'message': f'Файл успешно загружен: {file_name}'
        }
        return render(request, 'requestdataapp/file-uploadd.html',
                      context=context)

    return render(request, 'requestdataapp/file-uploadd.html')

