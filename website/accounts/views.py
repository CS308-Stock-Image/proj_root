from django.shortcuts import get_object_or_404, render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from .forms import *
import os
from django.contrib.auth.decorators import login_required


# Create your views here.
from .models import *
from .forms import  CreateUserForm
def home(request):
	photos =Photo.objects.all()
	context={'photos':photos}
	return render(request, 'accounts/main.html',context)
def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)
                

				return redirect('login')

		context = {'form':form}
		return render(request, 'accounts/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def gallery(request):
    user = request.user
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.filter(category__user=user)
    else:
        photos = Photo.objects.filter(
            category__name=category, category__user=user)

    categories = Category.objects.filter(user=user)
    context = {'categories': categories, 'photos': photos}
    return render(request,  'accounts/photos/gallery.html', context)


@login_required(login_url='login')
def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'accounts/photos/photo.html', {'photo': photo})


@login_required(login_url='login')
def addPhoto(request):
    user = request.user

    categories = user.category_set.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                user=user,
                name=data['category_new'])
        else:
            category = None

        for image in images:
            photo = Photo.objects.create(
                category=category,
                category_name=category,
                description=data['description'],
                image=image,
                price=data['price'],
            )

        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'accounts/photos/add.html', context)

def deletePhoto(request,pk):
    photo=Photo.objects.get(id=pk)
    photo.delete()
    return redirect('home')

def sortByCategory(request):
   photos =Photo.objects.all().order_by('category_name')
   context={'photos':photos}
   return render(request, 'accounts/main.html',context)

def sortByIncreasingPrice(request):
   photos =Photo.objects.all().order_by('price')
   context={'photos':photos}
   return render(request, 'accounts/main.html',context)

def sortByDecreasingPrice(request):
   photos =Photo.objects.all().order_by('-price')
   context={'photos':photos}
   return render(request, 'accounts/main.html',context)

def shopcart(request):
    image=ShopCart.objects.filter()
    context= {"image":image}
    return render(request,"accounts/cart.html",context)
    

def addtoshopcart(request,id):
  

    current_user=request.user
    data=ShopCart(id=id)

    if data.quantity==0:
        data.user_id =current_user.id
        data.product_id =id
        data.product= Photo(id=id)
        data.quantity=1
        data.save()
        image=ShopCart.objects.filter()
        context= {"image":image}
        return render(request,"accounts/cart.html",context)
   
    return redirect('home')

def deletecart(request,id):
    cart = ShopCart(id)
    cart.delete()
    return redirect('shopcart')

def checkout(request):
    return render(request,"accounts/checkout.html")



