from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import logout
from.forms import *
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def logout_view(request):
    logout(request)
    return redirect('home')


def home(request):
    context = {'blogs': Blog.objects.all()}
    return render(request, 'home.html', context)


def login_view(request):
    return render(request, 'login.html')


def blog_detail(request, slug):
    context = {}
    try:
        blog_obj = Blog.objects.filter(slug=slug).first()
        context['blog_obj'] = blog_obj
    except Exception as e:
        print(e)
    return render(request, 'blog_detail.html', context)


def see_blog(request):
    context = {}

    try:
        blog_objs = Blog.objects.filter(user=request.user)
        context['blog_objs'] = blog_objs
    except Exception as e:
        print(e)

    print(context)
    return render(request, 'see_blog.html', context)


def add_blog(request):
    context = {'form': BlogForm}
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST)
            print(request.FILES)
            image = request.FILES.get('image', '')
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                print('Valid')
                content = form.cleaned_data['content']

            blog_obj = Blog.objects.create(
                user=user, title=title,
                content=content, image=image
            )
            print(blog_obj)
            return redirect('/add-blog/')
    except Exception as e:
        print(e)

    return render(request, 'add_blog.html', context)


def blog_update(request, slug):
    context = {}
    try:

        blog_obj = Blog.objects.get(slug=slug)

        if blog_obj.user != request.user:
            return redirect('/')

        initial_dict = {'content': blog_obj.content}
        form = BlogForm(initial=initial_dict)
        if request.method == 'POST':
            form = BlogForm(request.POST)
            print(request.FILES)
            image = request.FILES['image']
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']

            blog_obj = Blog.objects.create(
                user=user, title=title,
                content=content, image=image
            )

        context['blog_obj'] = blog_obj
        context['form'] = form
    except Exception as e:
        print(e)

    return render(request, 'update_blog.html', context)


def blog_delete(request, id):
    try:
        blog_obj = Blog.objects.get(id=id)

        if blog_obj.user == request.user:
            blog_obj.delete()

    except Exception as e:
        print(e)

    return redirect('/see-blog/')


def register_view(request):
    return render(request, 'register.html')


def verify(request, token):
    try:
        profile_obj = Profile.objects.filter(token=token).first()

        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
        return redirect('/login/')

    except Exception as e:
        print(e)

    return redirect('/')


def send(request):
    if request.method == 'POST':
        to = request.POST.get('toemail')
        content = request.POST.get('content')
        # print(to,content)
        send_mail(
            # subject
            'texting',
            # msg
            content,
            # from email
            settings.EMAIL_HOST_USER,
            # rec list
            [to]

        )
        return HttpResponse('Email send successfully!!')
    return render(request,'sendEmail.html',{'title':'sendEmail'})