from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Bar, Beverage, Review, Photo
from botocore.exceptions import ClientError
import uuid
import boto3
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import ReviewForm
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

# Change this to yours
S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET='softwaredev'

@login_required
def add_photo(request, bar_id):
   photo_file = request.FILES.get('photo-file', None)
   if photo_file:
      s3 = boto3.client('s3')
      key = 'barfly/' + uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      try:
         s3.upload_fileobj(photo_file, BUCKET, key)
         url = f'{S3_BASE_URL}{BUCKET}/{key}'
         Photo.objects.create(url=url, bar_id=bar_id)
      except ClientError as e:
         print(e, " error from aws!")
      return redirect('detail', bar_id=bar_id)
      
@login_required
def add_review(request, bar_id):
  form = ReviewForm(request.POST)
  if form.is_valid():
      new_review = form.save(commit=False)
      new_review.bar_id = bar_id
      new_review.user = request.user
      new_review.save()
  return redirect('detail', bar_id=bar_id)

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def bars_index(request):
    bars = Bar.objects.all()
    return render(request, 'bars/index.html', {'bars': bars})

def bars_detail(request, bar_id):
    bar = Bar.objects.get(id=bar_id)
    bar.site_traffic += 1
    bar.save()
    beverages_bar_doesnt_have = Beverage.objects.exclude(id__in = bar.beverages.all().values_list('id'))
    review_form = ReviewForm()
    return render(request, 'bars/detail.html', {'bar': bar, 'review_form': review_form, 'beverages': beverages_bar_doesnt_have})

class BarCreate(LoginRequiredMixin, CreateView):
    model = Bar
    fields = ['name', 'address', 'theme', 'has_cover']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class BarUpdate(LoginRequiredMixin, UpdateView):
   model = Bar
   fields = ['name', 'address', 'theme', 'has_cover']


@login_required
def assoc_beverage(request, bar_id, beverage_id):
	Bar.objects.get(id=bar_id).beverages.add(beverage_id)
	return redirect('detail', bar_id=bar_id)

@login_required
def un_assoc_beverage(request, bar_id, beverage_id):
	Bar.objects.get(id=bar_id).beverages.remove(beverage_id)
	return redirect('detail', bar_id=bar_id)

class BeverageList(ListView):
  model = Beverage

class BeverageDetail(DetailView):
  model = Beverage

class BeverageCreate(LoginRequiredMixin, CreateView):
  model = Beverage
  fields = ['bev_name', 'ingredients', 'price', 'is_alcohol', 'img']
  
  def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
  success_url = '/bars/'

class BeverageUpdate(LoginRequiredMixin, UpdateView):
  model = Beverage
  fields = '__all__'

class BeverageDelete(LoginRequiredMixin, DeleteView):
  model = Beverage
  success_url = '/bars/'

class ReviewDelete(LoginRequiredMixin, DeleteView):
   model = Review
   success_url = '/bars/'
