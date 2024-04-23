from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm
# login logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,login,logout


# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # check if forms are valid then do something
        if user_form.is_valid() and profile_form.is_valid():
            # save form infor to user obbject, hash the password and append to the user obbject
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # set commit to false to avoid collision with previously saved data
            profile = profile_form.save(commit=False)
            # in the views we define the one-to-one rekationship as defined in models as follows
            profile.user = user
            # check if profile image was uploaded

            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']

            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basic_app/registration.html',
                            {'user_form':user_form,
                             'profile_form':profile_form,
                             'registered':registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate using built-in method
        user = authenticate(username=username,password=password)

        if user:
            # i.e authenticated
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account not active')
        else:
            print('Someone tried to login and failed')
            print("Username: {} and password: {}".format(username,password))
            return HttpResponse('Invalid login details!')

    else:
        return render(request,'basic_app/login.html',{})
