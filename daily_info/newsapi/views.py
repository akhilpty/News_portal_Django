from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from admin_news.forms import RegisterForm, AddForm, UpdateForm

from .serializer import NewsSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
)

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from admin_news.models import News


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def loginapi(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def signupapi(request):
    registerform = RegisterForm(request.data)
    if registerform.is_valid():
        username = registerform.cleaned_data['username']
        email = registerform.cleaned_data['email']
        password = registerform.cleaned_data['password']
        if User.objects.filter(username=username).exists():
            registerform = RegisterForm(request.POST)
            context = {'username': username,
                       'error': 'Username already exists add a new one'}
            return Response(context, status=HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password,
                                            )
            user.save()
            context = {'registerform': registerform.data,
                       'success': 'Created user'}
            return Response(context, status=HTTP_200_OK)
    else:
        registerform = RegisterForm(request.POST)
        context = {'registerform': registerform.data,
                   'errors': registerform.errors}
        return Response(context, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def listapi(request):
    news = News.objects.all()
    content = NewsSerializer(news, many=True)
    return Response(content.data, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def addapi(request):
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
            newsSer = NewsSerializer(news_data)

            return Response(newsSer.data, status=HTTP_200_OK)
        else:
            form = AddForm(request.POST)
            context = {'form': form.data,
                       'errors': form.errors}
            return Response(context, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["PUT"])
@permission_classes((IsAuthenticated,))
def updatenewsapi(request,id):
    news_cont = get_object_or_404(News, id=id)
    form = UpdateForm(request.POST, request.FILES, instance=news_cont)
    if form.is_valid():
            form.save()
      
            return Response({'form':form.data,"message":"Success"}, status=HTTP_200_OK)
    else:
        form = UpdateForm(request.data)
        context = {'form': form.data, 'errors': form.errors}
        return Response(context, status=HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(["DELETE"])
@permission_classes((IsAuthenticated,))       
def deletenewsapi(request, id):
    news_cont = get_object_or_404(News, id=id)
    news_cont.delete()
    return Response({"Message":"The Content is Successfully Deleted"}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def searchapi(request):
    searchnews= request.query_params.get('search', '')
    if searchnews:
        allNews=News.objects.filter(title__istartswith=searchnews)
        if not allNews:
            return Response({"No item with your search", searchnews}, status=HTTP_204_NO_CONTENT)
        else:
            serializer = NewsSerializer(allNews, many=True)
            return Response(serializer.data, status=HTTP_200_OK)

    else:
        news=News.objects.all()
        serializerfilter = NewsSerializer(news, many=True)
        return Response(serializerfilter.data, status=HTTP_204_NO_CONTENT)