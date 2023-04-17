from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .models import Bar
from botocore.exceptions import ClientError
import uuid
import boto3
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'

  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def bars_index(request):
    bars = Bar.objects.filter(user=request.user)
    return render(request, 'bars/index.html', {'bars': bars})

class BarCreate(CreateView):
    model = Bar
    fields = ['name', 'address', 'theme', 'site_traffic', 'has_cover']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)