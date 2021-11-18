from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

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

                return HttpResponseRedirect('/')

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


class RegistrationView(View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {'form': form}

        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):

        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)

            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.phone = form.cleaned_data['phone']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {'form': form}
        return render(request, 'registration.html', context)


def user_logout(request):
    request.user.set_unusable_password()
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def main(request):
    context = {}
    files = Files.objects.filter(author_id=request.user.id)
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
                fs = FileSystemStorage(location='/home/gekk0/migoogledrive/testvideo',
                                       file_permissions_mode=None, directory_permissions_mode=None)

                name = fs.save(uploaded_file.name, uploaded_file)
                context['url'] = fs.url(name)
                context['fs_location'] = str(fs.location)

                file = Files.objects.create(name=uploaded_file.name, url=fs.url(name))
                file.size = fs.size(name) / 1000000
                file.author = request.user
                file.save()

                messages.success(request, 'Файл '+file.name+' был загружен')

                if bool(request.FILES.get('poster', False)):
                    file.poster = request.FILES['poster']
                    file.save()

        except:
            messages.warning(request, 'Файл не был отправлен')

    return HttpResponseRedirect('/')


def delete(request, video_id):

    file = Files.objects.get(id=video_id)
    fs = FileSystemStorage(location='/home/gekk0/migoogledrive/testvideo',
                           file_permissions_mode=None, directory_permissions_mode=None)
    fs.delete(file.name)
    file.delete()
    messages.info(request, 'Файл ' + file.name + ' был удален')

    return HttpResponseRedirect('/')
