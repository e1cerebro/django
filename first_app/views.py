from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from first_app.models import AccessRecord, Topic, Webpage
from . import forms
from first_app.forms import NewTopicForm, UserProfileInfoForm, UserForm
from django.contrib.auth.forms import User


# Imports for login
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    access_records = AccessRecord.objects.order_by('date')
    data = {"access_records": access_records}
    return render(request, 'first_app/index.html', data)


def user_login(request):

    # Check if the user posted login info

    if request.method == 'POST':

        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate the user
        user = authenticate(username=username, password=password)

        # If the user was authenticated
        if user:
            if user.is_active:
                login(request, user)
                # Redirect the user if they are logged in
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("Account In active")
        else:
            print("Somee tired to login and failed")
            return HttpResponse("Invalid user login details")
    else:
        return render(request, 'first_app/login.html',{})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('/index/'))


def register(request):

    registered = False

    if request.method == 'POST':
        # Grab the data from the POST
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check if the form is valid and save the user data
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # Hash the user password
            user.set_password(user.password)
            # Save the latest data
            user.save()

            # commit the profile information without saving them: This is because we havent
            # checked if the user provided an image(profile pics)
            profile = profile_form.save(commit=False)
            # Set the user id. this is used to fulfile the OneToOneField
            # Registered on our Form.py file
            profile.user = user

            if 'profile_pics' in request.FILES:
                profile.profile_pics = request.FILES['profile_pics']

                profile.save()

                registered = True

            else:
                print(user_form.errors, profile_form.errors)
    else:
            user_form = UserForm()
            profile_form = UserProfileInfoForm()

    return render(request, 'first_app/registration.html',
                      {"profile_form": profile_form, 'user_form': user_form, 'registered': registered})


def showform(request):

    if request.method == 'POST':
        topicForm = forms.TopicForm(request.POST)
        if topicForm.is_valid():
            data = {
                'TopicForm': topicForm,
                "status": "success",
                "form_data_name": topicForm.cleaned_data['name'],
                "form_data_email": topicForm.cleaned_data['email'],
                "form_data_message": topicForm.cleaned_data['message'],
            }
        else:
            print('Invalid form')
            data = {'TopicForm': topicForm}
        return render(request, 'first_app/my_form.html', data)
    else:
        topicForm = forms.TopicForm()
        data = {'TopicForm': topicForm}
        return render(request, 'first_app/my_form.html', data)


def newtopic(request):

    new_topic_form = NewTopicForm()
    topics = Topic.objects.order_by('top_name')

    if request.method == 'POST':
        new_topic_form = NewTopicForm(request.POST)

        if new_topic_form.is_valid():
            new_topic_form.save(commit=True)
            return render(request, "first_app/topics.html", {'form': new_topic_form, 'topics':topics})
        else:
            print("Invalid form")

    return render(request, "first_app/topics.html", {'form': new_topic_form, 'topics':topics})

