import datetime

import jwt
from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from blog.forms import UserRegisterForm, UserLoginForm
from .models import User
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer, )



class LogoutView(APIView):
    def get(self,request):
        logout(request)
        return redirect('home')
    def post(self,request):
        responsce = Response()
        responsce.delete_cookie('jwt')
        responsce.data = {
             'message':'success'
        }
        return responsce

class RegistrationAPIView(APIView):
    """
    Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
    """
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    def get(self,request):
        form = UserRegisterForm(request.POST)
        return render(request, 'authentication/register.html', {'form': form})
    def post(self, request):
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'Вы успешно зарегистрировались!')
                return redirect('home')
            else:
                messages.error(request, 'Ошибка регистрации')
        else:
            form = UserRegisterForm()
        # Паттерн создания сериализатора, валидации и сохранения - довольно
        # стандартный, и его можно часто увидеть в реальных проектах.
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Create your views here.
class LoginAPIView(APIView):
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def get(self,request):
        form = UserLoginForm()
        return render(request,'authentication/login.html', {'form': form})
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        payload = {
            'pk':user.pk,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
        token = jwt.encode(payload,'secret',algorithm='HS256').decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data = {
            'jwt':token
        }

        return response

        # Обратите внимание, что мы не вызываем метод save() сериализатора, как
        # делали это для регистрации. Дело в том, что в данном случае нам
        # нечего сохранять. Вместо этого, метод validate() делает все нужное.


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get('jwt')
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        if not token:
            raise AuthenticationFailed('Пользователь не авторизирован')
        try:
            payload = jwt.decode(token,'secret',algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Пользователь не авторизирован')

        user = User.objects.filter(id = payload['pk']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)
