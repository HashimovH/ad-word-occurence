from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from advertisement.forms import AudioUploadForm
from advertisement.models import AudioFile
from advertisement.utils import count_occurrences, transcribe_audio

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'advertisement/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'advertisement/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home_view(request):
    executions = AudioFile.objects.filter(
        user=request.user).order_by('-created_at')
    return render(request, 'advertisement/home.html', {"executions": executions})


@login_required
def upload_audio(request):
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            audio = form.save(commit=False)
            audio.user = request.user
            audio.word_count = 0
            # Save result
            audio.save()

            # Process audio
            transcription = transcribe_audio(audio.file.path)
            count = count_occurrences(transcription, audio.search_term)
            audio.word_count = count
            audio.save()

            return redirect('home')
    else:
        form = AudioUploadForm()

    return render(request, 'advertisement/upload_audio.html', {'form': form})
