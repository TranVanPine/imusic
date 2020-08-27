from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import UserUpdateForm, ProfileUpdateForm
from .forms import RegisterForm
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import CreateView, DetailView, DeleteView, ListView
from .models import *
from .forms import SongUploadForm
from tinytag import TinyTag
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.shortcuts import render


def index(request):
    context = {
        'artists' : Artist.objects.all(),
        'genres': Category.objects.all()[:6],
        'latest_songs': Song.objects.all()[:6]
    }  
    return render(request, "index.html", context)

class CategoryListView(ListView):
    model = Category

class CategoryDetailView(DetailView):
    model = Category


class SongListView(ListView):
    model = Song


class SongDetailView(DetailView):
    model = Song

class ArtistDetailView(DetailView):
    model = Artist

class ArtistListView(ListView):
    model = Artist


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Successful!!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'registration/profile.html', context)


class HotSongListView(ListView):
    model = Song
    template_name = 'myalbums/hot_music.html'
    context_object_name = 'songs'

class SongUploadView(CreateView):
    form_class = SongUploadForm
    template_name = "songs/create.html"

    @method_decorator(login_required(login_url=reverse_lazy('index')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SongUploadView, self).get_context_data(**kwargs)
        context['artists'] = Artist.objects.all()
        context['category'] = Category.objects.all()
        return context


    def post(self, request, *args, **kwargs):

        form = self.get_form()
        print(form)
        if form.is_valid():

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=200)

    def form_valid(self, form):
        song = TinyTag.get(self.request.FILES['song'].file.name)
        form.instance.playtime = song.duration
        form.instance.size = song.filesize
        artists = []
        for a in self.request.POST.getlist('artists[]'):
            try:
                artists.append(int(a))
            except:
                artist = Artist.objects.create(name=a)
                artists.append(artist)
        form.save()
        form.instance.artist.set(artists)
        form.save()
        data = {
            'status': True,
            'message': "Successfully submitted form data.",
            'redirect': reverse_lazy('upload-details', kwargs={'id': form.instance.id})
        }
        return JsonResponse(data)

class SongUploadDetailsView(DetailView):
    model = Song
    template_name = 'songs/show.html'
    context_object_name = 'song'
    slug_field = 'id'
    slug_url_kwarg = 'id'

class SongDetailView(DetailView):
    model = Song

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')
        data = {'username':username,'email': email, 'password1': password1, 'password1': password2}
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(password1)
            form.save()
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


