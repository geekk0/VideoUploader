import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from VideoUploader import settings
from videofiles.forms import LoginForm, ResetPassword, RegistrationForm
from videofiles.models import Files


class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {'form': form}
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)

                return HttpResponseRedirect('/viewer')

        return render(request, 'login.html', {'form': form})


class ResetPasswordView(View):

    def get(self, request, *args, **kwargs):
        form = ResetPassword(request.POST or None)
        form.initial['username'] = request.user.username
        context = {'form': form}
        return render(request, 'password_reset.html', context)

    def post(self, request, *args, **kwargs):
        current_user = request.user
        form = ResetPassword(request.POST or None)
        uid = request.user.username

        if form.is_valid():
            current_user.set_password(form.cleaned_data['new_password'])
            current_user.save()
            return HttpResponseRedirect('/')
        return render(request, 'password_reset.html', {'form': form})


def user_logout(request):
    request.user.set_unusable_password()
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def main(request):
    context = {}
    files = Files.objects.all()
    context['files'] = files

    user_agent = request.META['HTTP_USER_AGENT']

    if 'Mobile' in user_agent:
        return render(request, 'mobile_main.html', context)
    else:
        return render(request,  'main.html', context)


def upload(request):
    context = {}

    if request.method == 'POST':
        try:
            if bool(request.FILES.get('video', False)):
                uploaded_file = request.FILES['video']
                form = request.POST
                fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'original'),
                                       file_permissions_mode=None, directory_permissions_mode=None)
                name = fs.save(uploaded_file.name, uploaded_file)
                context['url'] = fs.url(name)
                context['fs_location'] = str(fs.location)

                file = Files.objects.create(name=uploaded_file.name, url=fs.url(name))
                file.size = fs.size(name) / 1000000
                file.author = form['username']
                if form['contact_info']:
                    file.contact_info = form['contact_info']
                file.proxy_file = file.name[:-3]+'mp4'
                file.proxy_file_url = file.url[:-3]+'mp4'
                file.save()

                messages.success(request, 'Файл ' + file.name + ' был загружен')

        except:
            messages.warning(request, 'Файл не был отправлен')

        return HttpResponseRedirect('/')


def delete(request, video_id):

    file = Files.objects.get(id=video_id)

    fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'original'),
                               file_permissions_mode=None, directory_permissions_mode=None)
    fs.delete(file.name)

    proxy_fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'web'),
                               file_permissions_mode=None, directory_permissions_mode=None)
    proxy_fs.delete(file.proxy_file)
    print(proxy_fs)

    file.delete()
    messages.info(request, 'Файл ' + file.name + ' был удален')

    return HttpResponseRedirect('/viewer')


def file_upload(request):
    context = {}

    return render(request,  'upload_file.html', context)


"""def convert_to_mp4(fs, file_name):
    os.system('ffmpeg -i '+fs.path(file_name)+' '+fs.path(file_name)[:-3]+'mp4')"""



