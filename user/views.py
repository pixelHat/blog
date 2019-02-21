from django.shortcuts import render


def index(request):
    return render(request, 'user/index.html')


def post(request):
    return render(request, 'user/post.html')
