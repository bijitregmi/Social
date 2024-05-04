import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from rest_framework.decorators import api_view

from .forms import NewPostForm
from .models import Follow, Post, User
from .serializers import PostSerializers


def index(request):
    posts = Post.objects.all().order_by("-created_at")
    new_post_form = NewPostForm()

    # Apply paginaiton to posts
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    posts_view = paginator.get_page(page_number)

    # Save new post
    if request.method == "POST":
        new_post_form = NewPostForm(request.POST)
        if new_post_form.is_valid():
            new_post = new_post_form.save(commit=False)
            new_post.poster = request.user
            new_post.save()
            return HttpResponseRedirect(reverse("network:index"))

        # Error validation in new post
        else:
            return render(
                request,
                "network/index.html",
                {
                    "new_post_form": new_post_form,
                    "posts": posts_view,
                    "message": "Invalid Post",
                },
            )

    # Display all posts
    return render(
        request,
        "network/index.html",
        {"new_post_form": new_post_form, "posts": posts_view},
    )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")


@login_required(login_url="network:login")
def profile(request, pk):

    # Get user profile details
    viewed_user = User.objects.get(pk=pk)
    current_user = request.user
    user_following = Follow.objects.filter(followed_by=current_user).values_list(
        "following", flat=True
    )
    posts = Post.objects.filter(poster=viewed_user)

    # Apply paginaiton to posts
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    posts_view = paginator.get_page(page_number)

    return render(
        request,
        "network/profile.html",
        {
            "viewed_follower_count": Follow.objects.filter(
                following=viewed_user
            ).count(),
            "viewed_following_count": Follow.objects.filter(
                followed_by=viewed_user
            ).count(),
            "user_following": user_following,
            "viewed_user": viewed_user,
            "posts": posts_view,
        },
    )


@login_required(login_url="network:login")
def follow(request, pk):
    viewed_user = User.objects.get(pk=pk)
    current_user = request.user

    # Follow or unfollow user
    if request.method == "POST":
        if "follow" in request.POST:
            new_follow = Follow.objects.create(
                following=viewed_user, followed_by=current_user
            )
            new_follow.save()
        else:
            follow = Follow.objects.get(following=viewed_user, followed_by=current_user)
            follow.delete()

    return HttpResponseRedirect(reverse("network:profile", kwargs={"pk": pk}))


@login_required(login_url="network:login")
def following(request):

    # Show only following posts
    follow = Follow.objects.filter(followed_by=request.user).values_list("following")
    new_post_form = NewPostForm()

    # Apply paginaiton to posts
    posts = Post.objects.filter(poster__in=follow).order_by("-created_at")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    posts_view = paginator.get_page(page_number)

    return render(
        request,
        "network/index.html",
        {"posts": posts_view, "new_post_form": new_post_form},
    )


@login_required(login_url="network:login")
@api_view(["GET", "PUT"])
def edit(request, pk):

    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "PUT":
        # Validate user
        if request.user == post.poster:

            # Get data
            data = json.loads(request.body)

            # Serialize and save data
            serializer = PostSerializers(post, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)

        return JsonResponse({"error": "User not authorized"}, status=401)

    # Send post value
    elif request.method == "GET":
        serializer = PostSerializers(post)
        return JsonResponse(serializer.data, status=200)


@login_required
@api_view(["PUT"])
def like(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=404)

    data = json.loads(request.body)

    # Add or remove user from post
    if data.get("liked"):
        post.liked_by.add(request.user)
        post.likes = post.liked_by.all().count()
        post.save()

    else:
        post.liked_by.remove(request.user)
        post.likes = post.liked_by.all().count()
        post.save()

    # Send value
    serializer = PostSerializers(post)
    return JsonResponse(serializer.data, status=200)
