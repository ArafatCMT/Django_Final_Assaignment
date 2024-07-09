from django.shortcuts import render, redirect
from rest_framework.views import APIView
from . import serializers
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework import status
from .models import Account
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework import generics

# Create your views here.
class is_authenticated(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False
        return True


class RegistrationView(APIView):
    permission_classes = [is_authenticated] # authenticated user hoile register page er permission nai
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            user = serializer.save()

            # confirmation mail ta ke strong korar jonno token and uid user korta ci 
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            verification_link = f"http://127.0.0.1:8000/accounts/verify/{token}/{uid}"

            email_subject = "Verify Your Account"
            email_body = render_to_string('Verification_mail.html', {'verification_link': verification_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()

            return Response("Check your email for confirmation", status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    

def is_active(request, token, uid64):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid) # decode korar por jei uid ta pelam ei uid ta kon user er primary_key oi user ta ke get kortaci
    except(User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        return redirect('login')
    return redirect('register')

class LoginView(APIView):
    permission_classes = [is_authenticated] # authenticated user hoile login page er permission nai
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data = self.request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            # print(username, password)

            user = authenticate(username=username, password=password)
            print(user)

            if user:
                token, _ = Token.objects.get_or_create(user=user)
                # print(token)
                # print(_)
                login(request, user)
                return Response({'token': token.key, 'user_id': user.id})
            else:
                return Response({'error': "Invalid Credential"})
        return Response(serializer.errors)


class LogoutView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            logout(request)
            return redirect('login')
        return redirect('login')

# class ProfileView(APIView):
#     permission_classes = [IsAuthenticated]
        
#     def get(self, request, format=None):
#         account = Account.objects.all()
#         serializer = serializers.ProfileSerialize(account, many=True)
#         return Response(serializer.data)
    
class EditProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ProfileSerialize

    def get_objects(self, pk):
        try:
            user = User.objects.get(pk=pk)
            account = Account.objects.get(user=user)
        except(Account.DoesNotExist):
            account = None

        if account is not None:
            return account
        return Http404
        
    def get(self, request, format=None):
        account = self.get_objects(request.user.id)
        serializer = serializers.ProfileSerialize(account)
        return Response(serializer.data)
    
    def put(self, request, format=None):
        account = self.get_objects(request.user.id)
        serializer = self.serializer_class(account, data=request.data)
        
        if serializer.is_valid():
            if serializer.validated_data['image'] is None:
                serializer.validated_data['image'] = account.image
                # print(serializer.validated_data['image'])

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProfileListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Account.objects.all()
    serializer_class = serializers.ProfileSerialize
    
    

            





