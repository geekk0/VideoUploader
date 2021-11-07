from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render

from videofiles.models import Files


def main(request):
    context = {}

    return render(request,  'base.html', context)


def upload(request):
    context = {}
    files = Files.objects.all()
    context['files'] = files

    if request.method == 'POST':
        if bool(request.FILES.get('video', False)):
            uploaded_file = request.FILES['video']
            fs = FileSystemStorage(location='/run/user/1000/gvfs/smb-share:server=192.168.101.91,share=temp/testvideo',
                                   file_permissions_mode=None, directory_permissions_mode=None)
            name = fs.save(uploaded_file.name, uploaded_file)
            context['url'] = fs.url(name)
            context['fs_location'] = str(fs.location)

            file = Files.objects.create(name=uploaded_file.name, url=fs.url(name))
            file.size = fs.size(name)/1000000
            file.save()
            if bool(request.FILES.get('poster', False)):
                file.poster = request.FILES['poster']
                file.save()

    return render(request, 'base.html', context)


def delete(request, video_id):
    context = {}
    file = Files.objects.get(id=video_id)
    fs = FileSystemStorage(location='/run/user/1000/gvfs/smb-share:server=192.168.101.91,share=temp/testvideo',
                           file_permissions_mode=None, directory_permissions_mode=None)
    fs.delete(file.name)
    file.delete()

    return HttpResponseRedirect('/')



