from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm,MyUserCreationForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout



# View for handling Login Page.

def LoginPage(request):
    # If someone trys to login with form having method Post
    if request.method == "POST":

        # Getting the email filled by user
        email = request.POST.get("email").lower()
        # getting the psssword
        password = request.POST.get("password")
        try:
            # trying to find a user with exact filledmail in Model.
            user = User.objects.get(email=email)
        except:
            # If user not found or any error happened flashing message.
            messages.error(request, "User does not exists")
        
        # Authenticating user with enter email and password.
        # If successfully authenticated return the user object, else return None
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Getting user logged in and redirecting user to home page
            login(request, user)
            return redirect("Home")
        # else flashing another message.
        else:
            messages.error(request, "User Name or Password is wrong")
    # rendering  login page.
    return render(request, "base/login.html")

def RegisterPage(request):
    # A django Model form that generate a HTML form based on the model we have created
    form = MyUserCreationForm()

    # Going to render this form using for loop in template.
    context = {'form': form}

    if request.method == 'POST':
        # it will create the form filled with all the data that is recived in post request
        form = MyUserCreationForm(request.POST)
        if form.is_valid(): # check wheather the form filled by user is valid according to the model.
            # commit false will frezz the change 
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.save()
            # After that login the user and redirecting the user to home page.
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, "An error occured, please fill the details properly")
    return render(request, 'base/signup.html', context)

def LogoutPage(request):
    logout(request)
    return redirect("Home")

# Rendering home page.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # Getting all the room whoes topic name or name or description conatains q
    # if q is empty getting all the rooms
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
        )

    # Getting 5 recent messages from rooms having topic name given in q(if any ove searched)
    # Else getting 5 recent messages from all the messages
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains = q)
    )[0:5]

    # Getting 5 topics from the topics Model
    topics = Topic.objects.all()[0:5]

    # Passing all data to the template
    context = {'rooms': rooms, 'topics': topics, 'room_messages': room_messages}
    return render(request, 'base/index.html', context)

def room(request, pk):
    room = Room.objects.get(id = pk)

    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('message')
        )

        room.participants.add(request.user)
        return redirect('Room', pk=room.id)


    context = {'room' : room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

# If person is not logined this will redirect the person to the url with name login
@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
            topic_name = request.POST.get("topic")
            # Return topic and True if topic already exists else return ne created topic and false.
            topic, created = Topic.objects.get_or_create(name=topic_name)
            Room.objects.create(
                host = request.user,
                topic = topic,
                name = request.POST.get("name"),
                description = request.POST.get("description")
            )
            return redirect('Home') 
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id = int(pk))
    topics = Topic.objects.all()
    if room.host != request.user:
        return HttpResponse("You are not allowed here!!")
    if request.method == 'POST':
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get("name")
        room.topic = topic
        room.description = request.POST.get("description")
        room.save()
        return redirect("Home")
        
    form = RoomForm(instance=room)
    context = {'form': form, 'room':room,'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id = int(pk))

    if room.host != request.user:
        return HttpResponse("You are not allowed here!!")

    if request.method == "POST":
        room.delete()
        return redirect("Home")
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url = 'login')
def delete_message(request, pk):
    messages = Message.objects.get(id = int(pk))

    if messages.user != request.user:
        return HttpResponse("You are not allowed here!!")
    
    messages.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def profilePage(request, pk):
    user = User.objects.get(id = pk)
    topics = Topic.objects.all()
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url = 'login')
def edit_profile(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile-page", user.id)
        
    return render(request, 'base/edit-user.html', {'form': form})


def browse_topics(request):
    q =  request.GET.get('q') if (request.GET.get('q') != None) else ''
    topics = Topic.objects.filter(
        Q(name__icontains = q)
    )[0:6]
    return render(request, 'base/topics.html', {'topics': topics})

def recent_activity(request):
    room_messages = Message.objects.all()[0:3]
    return render(request, 'base/activity.html', {'room_messages': room_messages})