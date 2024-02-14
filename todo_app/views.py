from django.shortcuts import render,redirect, get_object_or_404
from todo_app.models import Todo, Category, Profile
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
import random

#authentication
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

#forms
from .forms import UserForm, ProfileModelForm, TodoModelForm, CategoryModelForm

from django.views.generic.base import RedirectView

# Create your views here.

@login_required(login_url='/login/')
def home_view(request):
    todos = Todo.objects.filter(is_active=True, user=request.user)
    completed_todos = Todo.objects.filter(is_active=False, user=request.user)
    context = dict(todos=todos, completed_todos=completed_todos)
    return render(request, 'todo_app/homepage.html', context=context)


# New Todo
@login_required(login_url='/login/')
def todo_entry_view(request):
    form = TodoModelForm(request.POST or None)
    form.fields['category'].queryset = Category.objects.filter(user=request.user)
    context = dict(form=form, title='New Todo', button_info='Save')
    if form.is_valid():
        form = form.save(commit=False)
        form.user = request.user
        form.save()
        return redirect(reverse('todo_app:todo_view', kwargs={'todo_slug':form.slug}))
    return render(request, 'registration/form.html', context=context)



def complete_todo(request):
    if request.method == "POST" and 'checkbox' in request.POST:
            checkbox_todo = request.POST.getlist('checkbox')
            for checkbox in checkbox_todo:
                Todo.objects.filter(title=checkbox).update(is_active=False)
            return redirect(reverse('todo_app:home'))
    else:
        return redirect(reverse('todo_app:home'))

def activate_task(request):
     if request.method == "POST" and 'checkbox' in request.POST:
        checkbox_todo = request.POST.getlist('checkbox')
        for checkbox in checkbox_todo:
            Todo.objects.filter(title=checkbox).update(is_active=True)
        return redirect(reverse('todo_app:home'))
     else:
          return redirect(reverse('todo_app:home'))

# todo detail
@login_required(login_url='/login/')
def todo_view(request, todo_slug):
     todo = get_object_or_404(Todo,slug=todo_slug, user=request.user)
     context = dict(todo=todo)
     return render(request, "todo_app/todo_detail.html", context)

# Edit Todo
@login_required(login_url='/login/')
def edit_todo_view(request, todo_slug):
    todo = get_object_or_404(Todo, slug=todo_slug, user=request.user)
    form = TodoModelForm(request.POST or None, instance=todo)
    form.fields['category'].queryset = Category.objects.filter(user=request.user)
    context = dict(form=form, title='Edit Todo', button_info='Save')
    if form.is_valid():
        form.save() # formu değil artık objeyi kaydediyoruz.
        messages.success(request,"You've succesfully edited your Todo.")
        return redirect(reverse('todo_app:todo_view', kwargs={'todo_slug':todo_slug}))
    return render(request, 'registration/form.html', context=context)


# Delete Todo
@login_required(login_url='/login/')
def delete_todo_view(request,todo_slug):
    todo = get_object_or_404(Todo,slug=todo_slug, user=request.user)
    todo.delete()
    messages.success(request, 'Todo Has Been Deleted Succesfully.')
    return redirect('todo_app:home')

# Create New Category
@login_required(login_url='/login/')
def create_category_view(request):
    form = CategoryModelForm(request.POST or None)
    context = dict(form=form, title='New Category', button_info='Save')
    if form.is_valid():
        title = form.cleaned_data.get('title')
        obj, created = Category.objects.get_or_create(title=title, user=request.user) # If there is the same category in the database, it will return obj instead of create it.
        return redirect(reverse('todo_app:category_detail', kwargs={'category_slug':obj.slug}))
    return render(request, 'registration/form.html', context=context)

# Edit Category
@login_required(login_url='/login/')
def edit_category_view(request,category_slug):
    category = get_object_or_404(Category, slug=category_slug, user=request.user)
    form = CategoryModelForm(request.POST or None, instance=category)
    context = dict(form=form, title=f"{category.title} Edit", button_info='save')
    if form.is_valid():
        form.save()
        messages.success(request,"You've succesfully edited Category")
        return redirect(reverse('todo_app:category_detail', kwargs={'category_slug':category_slug}))
    return render(request, 'registration/form.html', context)


# Delete Category
@login_required(login_url='/login/')
def delete_category_view(request,category_slug):
    category = get_object_or_404(Category, slug=category_slug, user=request.user)
    category.delete()
    messages.success(request, 'Category Has Been Deleted Succesfully.')
    return redirect('todo_app:home')

        

# category detail
@login_required(login_url='/login/')
def category_detail_view(request, category_slug):
     category = get_object_or_404(Category, slug=category_slug)
     todos = Todo.objects.filter(is_active=True, category=category, user=request.user)
     context = dict(category=category, todos=todos)
     return render(request, 'todo_app/category_detail.html', context)
     
     
# login
def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('todo_app:home'))
    if request.method == 'POST':
        if request.POST['username'] != '' and request.POST['password'] != '':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password) # eğer alınan bilgiler doğruysa validate edilirse authenticate returns User object.
            if user is not None:
                login(request, user)
                messages.info(request, f'{user.username} You are succesfully logged in.')
                return redirect('todo_app:home')
            
            else:
                messages.warning(request, f'Username or Passsword Incorrect. Please check and try again.')
                return render(request, 'registration/login.html', context={})
        else:
            messages.info(request, 'Your Username or password is empty. Please check and try again !')
            return render(request, 'registration/login.html', {})
    else:
        return render(request, 'registration/login.html', context={})
     

# logout
def logout_view(request):
    if request.user.is_authenticated:
        messages.info(request,f'{request.user.username} You succesfully logged out.')
        logout(request)
        return redirect(reverse('logout'))
    else:
        if request.META.get('HTTP_REFERER'):
            return redirect(request.META['HTTP_REFERER'])
        return redirect('todo_app:home')
    

# Signup
def signup_view(request):
    form = UserForm(request.POST or None)
    if form.is_valid(): # if form is not valid then view works like get request.
        password = form.cleaned_data.get('password')
        form_user = form.save(commit=False) # returns User object -> Thanks to UserForm
        form_user.set_password(password)
        form_user.save()
        Profile.objects.create(user=form_user)
        messages.success(request, 'You registration is succesfully completed !')
        return redirect('todo_app:home')

    return render(request, 'registration/form.html', {'form':form, 'title':'Signup Form', 'button_info':'Register'})


@login_required(login_url='/login/')
def profile_view(request, profile_slug):
    profile = get_object_or_404(Profile, slug=profile_slug)
    context = dict(profile=profile)
    return render(request, 'todo_app/profile_detail.html', context)


@login_required(login_url='/login/')
def profile_edit_view(request):
    user = request.user
    user_data = dict(first_name = user.first_name, last_name=user.last_name)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=user.profile, initial=user_data) # None gelirse ProfileModelForm Boş olarak oluşur.
    context = dict(form=form, title=f'{user.username} Profile Edit', button_info='Update')
    if request.method == 'POST': 
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            form.save()
            messages.success(request,'Your profile has been updated.')
            return redirect(reverse('todo_app:profile', kwargs={'profile_slug':user.profile.slug}))
    return render(request, 'registration/form.html', context)


# Delete Account
@login_required(login_url='/login/')
def delete_account_view(request):
    user = get_object_or_404(User, username=request.user.username)
    if request.method == 'POST':
        if request.POST.get('number') and request.POST.get('number') == request.session['random_int']:
            user.delete()
            messages.warning(request, 'Your Account Has Been Deleted :(')
            return redirect('todo_app:home')
        else:
            messages.info(request, 'Wrong validation number. Please check the number above and try again.')
    random_int = random.randint(2500,10000)
    request.session['random_int'] = random_int
    context = dict(user=user, random_int=random_int)
    return render(request, 'registration/delete.html', context=context)
    