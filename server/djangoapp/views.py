from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    '''
    renders the about us page
    '''
    return render(request, 'djangoapp/about.html', context={})



# Create a `contact` view to return a static contact page
def contact(request):
    '''
    renders the contact us page
    '''
    return render(request, 'djangoapp/contact.html', context={})

# Create a `login_request` view to handle sign in request
def login_request(request):
    '''
    log user in or render login page
    '''
    context = {}
    #handle post request (user clicked the login button)
    if request.method == 'POST':
        #get post data
        username = request.POST.get('username', False)
        password = request.POST.get('psw', False)
        #attempt to authenticate
        user = authenticate(username=username, password=password)
        if user is not None:
            #User is valid. call login method and redirect to index page
            login(request, user)
            return redirect('djangoapp:index')
        else:
            #User not registered or submitted incorrectly.
            #Show login page
            return render(request, 'djangoapp/user_login.html')
    else:
        #Not a post request. User wants to see the login page.
        #Show login page
        return render(request, 'djangoapp/user_login.html')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context={}
    name_taken=False
    # Evaluate request type
    if request.method == "GET":
        # If its a get request, the user clicked on a sign up button on the website.
        # Therefore show the sign up page.
        context['name_taken'] = False
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == "POST":
        # If it's a post request the user is submitting info to sign up.
        # First get the user information
        username = request.POST.get('username', False)
        firstname = request.POST.get('firstname', False)
        lastname = request.POST.get('lastname', False)
        password = request.POST.get('password', False)
        user_exist = False
        try:
            # check if the username already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # if not log that this is a new user
            logger.debug(f"{username} is a new user")
        #if it's a new user
        if not user_exist:
            #create user in auth_user table
            user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, password=password)
            #login user and redirecto to index page
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['name_taken'] = True
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":

        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
#     context = {}
#     if request.method == 'GET':
#         return render(request, 'djangoapp/dealer_details.html')


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
