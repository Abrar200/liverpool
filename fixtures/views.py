from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Players, News, Profile, Comment
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from .forms import UserRegisterForm, ProfileForm, CommentForm

def home(request):
    news = News.objects.all()
    return render(request, 'home.html', {'news': news})


def fixtures_view(request):
    credentials = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_CALENDAR_CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/calendar.readonly']
    )
    service = build('calendar', 'v3', credentials=credentials)

    # Change 'primary' to the desired Google Calendar ID
    events = service.events().list(calendarId='u6kmbrsrt5qr3r6gjrtsussomc@group.calendar.google.com').execute()
    
    fixtures = []
    for event in events['items']:
        fixture = {
            'summary': event['summary'],
            'start': event['start'].get('dateTime', event['start'].get('date')),
            'end': event['end'].get('dateTime', event['end'].get('date')),
            'location': event['location'],
        }
        fixtures.append(fixture)
    return render(request, 'fixtures.html', {'fixtures': fixtures})



def players(request):
    players = Players.objects.all()
    return render(request, 'players.html', {'players': players})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('/')
    else:
        form = UserRegisterForm()
        profile_form = ProfileForm()
    return render(request, 'register.html', {'form': form, 'profile_form': profile_form})

@login_required
def NewsDetailView(request, title):
    news = get_object_or_404(News, title=title)
    comments = Comment.objects.filter(news=news)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            comment = form.save(commit=False)
            comment.news = news
            comment.save()
            return redirect(request.path_info, news_id=news.id)
    else:
        form = CommentForm()
    return render(request, 'news_detail.html', {'news': news, 'comments': comments, 'form': form})


def PlayerDetailView(request, player):
    player = get_object_or_404(Players, name=player)
    context = {'player' : player}
    return render(request, 'player_detail.html',  context)


def honourview(request):
    return render(request, 'honours.html')


