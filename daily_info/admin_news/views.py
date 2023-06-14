
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import News
from .forms import AddForm, RegisterForm, UpdateForm, loginForm
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
def register_admin(request):
    message = ''
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if User.objects.filter(username=username).exists():
                form = RegisterForm()
                message = "Username already exist"
                return render(request, "register.html", {'message': message, "form": form})
            else:
                user = User.objects.create_user(username=username,
                                                email=email,
                                                password=password,
                                                )
                user.save()
                return HttpResponseRedirect(reverse('loginadmin'))
    else:
        form = RegisterForm()
        return render(request, "register.html", {"form": form})


def login_admin(request):
    form = loginForm()
    message = ''
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('homenews'))

            else:
                message = 'Login failed!'
    return render(request, 'login.html', context={'form': form, 'message': message})


def logout_admin(request):
    logout(request)
    return redirect('homenews')


@login_required(login_url='loginadmin')
def addnews(request):
    if request.method == 'POST':
        form = AddForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            photo = form.cleaned_data['photo']
            video = form.cleaned_data['video']
            user_id = request.user

            news_data = News(title=title, content=content,
                             photo=photo, video=video, user_id=user_id)
            news_data.save()

            return HttpResponseRedirect(reverse('homenews'))
        else:

            return HttpResponseRedirect(reverse('addnews'))
    else:
        form = AddForm()
        return render(request, 'addnews.html', {'form': form})


# def home(request):
#     new = News.objects.all()
#     paginator = Paginator(new, 3)
#     page = request.GET.get('page')
#     news_list = paginator.get_page(page)
    

#     return render(request, 'home.html', {'new': new,},)


class home(ListView):
    model=News
    template_name="home.html"
    context_object_name='new'
    paginate_by=4


@login_required(login_url='loginadmin')
def updatenews(request, id):

    Newsid = int(id)
    News_sel = News.objects.get(id=Newsid)
    if request.method == 'POST':
        form = UpdateForm(request.POST, request.FILES, instance=News_sel)
        if form.is_valid():
            form.save()
            return redirect('homenews')
    form = UpdateForm(instance=News_sel)
    return render(request, 'updatenews.html', {'form': form})


def detailnews(request, id):
    current_user = request.user.id
    Newsid = int(id)
    News_sel = News.objects.get(id=Newsid)
    return render(request, 'detail.html', {'News_sel': News_sel, 'current_user': current_user})

@login_required(login_url='loginadmin')
def mynewsdetail(request):
    current_user = request.user.id
    mydetail = News.objects.all()
  
    return render(request, 'mynews.html', {'mydetail': mydetail, 'current_user': current_user})


@login_required(login_url='loginadmin')
def deletenews(request, id):
    Newsid = int(id)
    News_sel = News.objects.get(id=Newsid)
    News_sel.delete()
    return redirect('homenews')

