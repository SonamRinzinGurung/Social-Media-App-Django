from attr import fields
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
import json
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import User, Posts, Likes, Follow





def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")




PostForm = forms.modelform_factory(Posts, fields=('post',), widgets={
    'post': forms.Textarea(attrs={
            'class': 'form-control',
            'style':"height: 100px",
            'placeholder': "What's on your mind?"
    })
}, labels={
    'post': ""
})


def index(request):
    posts = Posts.objects.all().order_by('-created_at')
    template = "network/index.html"
    
    paginator = Paginator(posts,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.user.is_authenticated:
        if(request.method == "POST"):
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.cleaned_data['post']
                created_by = request.user
                post = Posts(post=post, created_by=created_by)
                post.save()
                return render(request, template, {
                    "form": PostForm, "message": "Post created successfully!",
                    'page_obj':page_obj
                })
        return render(request, template,{
            "form":PostForm,
            'page_obj':page_obj

        })
    return render(request, template,{
        'page_obj':page_obj

    })
    
    
    
    
def all_posts(request):
    if request.user.is_authenticated:
        posts = Posts.objects.all().order_by('-created_at')
        paginator = Paginator(posts, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, "network/all_posts.html", {
            "page_obj": page_obj
        })
    else:
        return HttpResponseRedirect(reverse("login"))
    
    
    
def profile(request,username):

    
    user = User.objects.get(username=username)
    
    followers_count = len(Follow.objects.filter(following = user))
    following_count = len(Follow.objects.filter(follower = user))
    
    if request.user.is_authenticated:
        is_follower = Follow.objects.filter(follower = request.user, following = user)
    else:
        is_follower = False
    
    posts = Posts.objects.filter(created_by=user).order_by('-created_at')
    paginator = Paginator(posts,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    
    return render(request, "network/profile.html", {
        "profile_user": user,
        "page_obj": page_obj,
        "followers_count": followers_count,
        'following_count': following_count,
        'is_follower':is_follower
        
    })

    

@csrf_exempt
@login_required
def follow(request):
    if request.method != 'POST':
        return JsonResponse({'error':'POST request required.'}, status=400)
    
    data = json.loads(request.body)
    user = User.objects.get(id = data)
    
    is_follower = Follow.objects.filter(follower = request.user, following=user)
    
    if is_follower:
        is_follower.delete()
        is_follower = False
    
    else:
        follow = Follow(
            follower = request.user,
            following = user
        )
        follow.save()
        is_follower = True
        
    total_followers = len(Follow.objects.filter(following=user))
    
    return JsonResponse({'total_followers':total_followers,'is_follower':is_follower},status=201)

    

@login_required    
def following(request):
    user = request.user
    
    follow_list=[]
    
    following = Follow.objects.filter(follower = user)
    
    for person in following:
        follow_list.append(person.following)
        
    posts = Posts.objects.filter(created_by__in = follow_list).order_by('-created_at')
    
    paginator = Paginator(posts,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request,"network/following.html",{
        'page_obj':page_obj,
    })


# @csrf_exempt
@login_required
def edit(request):
    if request.method != 'POST':
        JsonResponse({'error':"POST request required."})
        
    data = json.loads(request.body)
    id = data.get('id','')
    updated_post = data.get('body','')
    
    post = Posts.objects.get(id = id)
    post.post = updated_post
    post.save()
    
    return JsonResponse({"message": "Post updated successfully."}, status=201)



@csrf_exempt
@login_required
def like(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required.'}, status=400)
    
    #Get Post
    data = json.loads(request.body)
    post = Posts.objects.get(id = data)
    
    
    #check of user has already liked the post
    
    liked = Likes.objects.filter(liked_by = request.user, liked_post = post)
    
    if liked:
        liked.delete()
        liked = False
        
    else:
        like = Likes(liked_by = request.user, liked_post = post,)
        like.save()
        liked = True
    
    like_count = len(Likes.objects.filter(liked_post = post))
    
    
    return JsonResponse({'like_count': like_count,'liked':liked}, status=201)
