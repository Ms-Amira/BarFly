from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Bar, Beverage, Review
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
    beverages_bar_doesnt_have = Beverage.objects.exclude(id__in = bar.beverages.all().values_list('id'))
    review_form = ReviewForm()
    return render(request, 'bars/detail.html', {'bar': bar, 'review_form': review_form, 'beverages': beverages_bar_doesnt_have})

class BarCreate(CreateView):
    model = Bar
    fields = ['name', 'address', 'theme', 'site_traffic', 'has_cover']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class BarUpdate(UpdateView):
   model = Bar
   fields = ['name', 'address', 'theme', 'has_cover']



def assoc_beverage(request, bar_id, beverage_id):
	Bar.objects.get(id=bar_id).beverages.add(beverage_id)
	return redirect('detail', bar_id=bar_id)


class BeverageList(ListView):
  model = Beverage

class BeverageDetail(DetailView):
  model = Beverage

class BeverageCreate(CreateView):
  model = Beverage
  fields = ['bev_name', 'ingredients', 'price', 'is_alcohol']
  
  def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
  success_url = '/bars/'

class BeverageUpdate(UpdateView):
  model = Beverage
  fields = '__all__'

class BeverageDelete(DeleteView):
  model = Beverage
  success_url = '/bars/'


class ReviewDelete(DeleteView):
   model = Review
   success_url = '/bars/'