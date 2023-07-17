from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import RegistrationSerializer, LoginSerializer, EmailVerificationSerializer, RequestPasswordResetEmailSerializer, LogoutSerializer
from users.models import User
from rest_framework.response import Response
from .tasks import send_email
from .models import OTP
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from wallet.models import Account

# Create your views here.

class RegistrationView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        account = Account.objects.create(
            user = user,
            balance = 0,
        )
        account.save()
        
        otp_code = OTP.generate_otp(user)
        email_subject = 'Email Verification code'
        email_body = f"Hi {user.username}, here is your sngle-use code to verify your account OTP is: {otp_code}"

        data = {'email_body': email_body,
                'to_email': user.email,
                'email_subject': email_subject
         }
        
        send_email(data)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class EmailVerificationView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            otp_code = serializer.validated_data['otp_code']
            if OTP.objects.filter(otp_code=otp_code, user=request.user).exists():
                user_id = request.user.id
                user = User.objects.get(id=user_id)
                user.is_verified = True
                user.save()
                return Response({'Email Successfully verified'}, status = status.HTTP_200_OK)
            else:
                return Response({'invalid OTP'}, status = status.HTTP_404_NOT_FOUND)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'success': True, 'message':'Logged out successfully'},status=status.HTTP_200_OK)