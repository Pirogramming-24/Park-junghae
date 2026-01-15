import threading
from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from apps.posts.services.ai.ocr_service import run_ocr
from apps.posts.services.ai.rules import parse_nutrition
from django.db import close_old_connections

def main(request):
    posts = Post.objects.all()

    search_txt = request.GET.get('search_txt')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if search_txt:
        posts = posts.filter(title__icontains=search_txt)

    try:
        if min_price:
            posts = posts.filter(price__gte=int(min_price))
        if max_price:
            posts = posts.filter(price__lte=int(max_price))
    except:
        pass

    return render(request, "posts/list.html", {
        "posts": posts,
        "search_txt": search_txt,
        "min_price": min_price,
        "max_price": max_price,
    })


def run_ocr_async(post_id):
    try:
        close_old_connections()

        post = Post.objects.get(id=post_id)

        texts = run_ocr(post.photo.path)
        nut = parse_nutrition(texts)

        for field in ["kcal", "carbs", "protein", "fat"]:
            if nut.get(field) is not None:
                setattr(post, field, nut[field])

        post.ocr_done = True
        post.save()

    except Exception as e:
        print("OCR ASYNC ERROR:", e)


def create(request):
    if request.method == "GET":
        return render(request, "posts/create.html", {"form": PostForm()})

    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save()

        if post.photo:
            threading.Thread(target=run_ocr_async, args=(post.id,)).start()

    return redirect("/")


def detail(request, pk):
    post = Post.objects.get(id=pk)
    return render(request, "posts/detail.html", {"post": post})


def update(request, pk):
    post = Post.objects.get(id=pk)

    if request.method == "GET":
        return render(request, "posts/update.html", {
            "form": PostForm(instance=post),
            "post": post,
        })

    form = PostForm(request.POST, request.FILES, instance=post)
    if form.is_valid():
        post = form.save()

        if post.photo:
            post.ocr_done = False
            post.save(update_fields=["ocr_done"])
            threading.Thread(target=run_ocr_async, args=(post.id,)).start()

    return redirect("posts:detail", pk=pk)


def delete(request, pk):
    Post.objects.get(id=pk).delete()
    return redirect("/")
