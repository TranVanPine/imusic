from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, DeleteView, ListView
from .models import Song, Artist, Category, Album, Review, User, Profile
# from utils.song_utils import generate_key
from .forms import UserUpdateForm, ProfileUpdateForm, LyricAddForm
from .forms import RegisterForm
from tinytag import TinyTag
from django.http import  HttpResponseRedirect
from tinytag import TinyTag
from django.views.generic.list import BaseListView
from .models import *
# from utils.song_utils import generate_key
from .forms import UserUpdateForm, ProfileUpdateForm

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
        'user': request.user,
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'registration/profile.html', context)


class ArtistDetailView(DetailView):
    model = Artist


class HotSongListView(ListView):
    model = Song
    template_name = 'myalbums/hot_music.html'
    context_object_name = 'songs'

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

class SearchSongListView(ListView):
    # template_name = 'myalbums/song_detail.html'
    model = Song
    def get_queryset(self):
        query = self.request.GET.get('search')
        if query :
            return  Song.objects.filter(title__icontains=query)
        else :
            return  Song.objects.all()

class StationListView(ListView):
    model = User
    template_name = 'myalbums/user_list.html'

@login_required()
def follow(request, pk):
    if request.method == 'GET':
        user = request.user
        to_user = get_object_or_404(User, pk=pk)
        is_followed = 0

        try:
            followed = Follow.objects.get(follower=user, following=to_user)
            if followed:
                is_followed = 1
        except:
            pass

        context = {
            'user': user,
            'to_user': to_user,
            'is_followed': is_followed,
        }
        return render(request, 'myalbums/user_detail.html', context=context)
    elif request.method == 'POST':
        user = request.user
        to_user = get_object_or_404(User, pk=pk)

        try:
            followed = Follow.objects.get(follower=user, following=to_user)
            if followed:
                followed.delete()
        except:
            follow = Follow(follower=user, following=to_user)
            follow.save()

        url = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(url)

@login_required()
def favorite(request, pk):
    if request.method == 'GET':
        user = request.user
        favorite = get_object_or_404(Song, pk=pk)
        is_favorite = 0

        try:
            favorited = Favorite.objects.get(user_favorite = user, song_favorite = favorite)
            if favorited:
                is_favorite= 1
        except:
            pass

        context = {
            'user': user,
            'favorite': favorite,
            'is_favorite': is_favorite,
        }
        return render(request, 'myalbums/song_detail.html', context=context)
    elif request.method == 'POST':
        user = request.user
        favorite = get_object_or_404(Song, pk=pk)

        try:
            favorited = Favorite.objects.get(user_favorite = user, song_favorite = favorite)
            if favorited:
                favorited.delete()
        except:
            favorited = Favorite(user_favorite = user, song_favorite = favorite)
            favorited.save()

        url = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(url)

class FavoriteListView(ListView):
    model = Song
    template_name = 'myalbums/favorite.html'

def addlyric(request, pk):
    user = request.user
    song = get_object_or_404(Song, pk=pk)
    # content = Lyric.content
    form = LyricAddForm()
    context = {
        'user': user,
        'song': song,
        # 'content': content,
        'form': form,
    }
    if request.method == 'POST':
            form = LyricAddForm(request.POST, initial={'user': user, 'song': song})
            if form.is_valid():
                form.save()
                return redirect('song-detail', pk)

    return render(request, 'myalbums/lyric_add.html', context)







