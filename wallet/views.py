from django.shortcuts import render
from .serializers import AccountSerializer, PaymentSerializer, TransactionSerializer, DepositSerializer, PaymentRequestSerializer
from rest_framework.views import APIView
from .models import Account, Payment, Transaction, PaymentRequest
from rest_framework import generics, status
from rest_framework.response import Response
from users.models import User
from django.db.models import Q


# Create your views here.

class WalletView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class WalletDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class WalletBalance(APIView):
    def get(self, request):
        queryset = Account.objects.get(user=request.user)
        balance = queryset.balance

        return Response({"message": balance}, status=status.HTTP_200_OK)


class TransferView(generics.GenericAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

class PaymentsView(generics.GenericAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get(self, request):
        queryset = Payment.objects.filter(account__user=request.user)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentDetail(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = Payment.objects.filter(account__user=self.request.user)
        return queryset
    
        
class TransactionHistory(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


    def get_queryset(self):
        queryset = Transaction.objects.filter(account__user=self.request.user)
        return queryset
    

class Transactiondetail(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        queryset = Transaction.objects.filter(account__user=self.request.user)
        return queryset
    

class DepositFunds(generics.GenericAPIView):
    serializer_class = DepositSerializer
    queryset = Account.objects.all()

    def post(self, request):
        serializer = DepositSerializer(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        resp = serializer.save()
        return Response(resp)
    
class PaymentRequestView(generics.GenericAPIView):
    queryset = PaymentRequest.objects.all()
    serializer_class = PaymentRequestSerializer


    def get(self, request):
        if request.GET.get('type') == 'sent':
            queryset = PaymentRequest.objects.filter(sender=request.user)
        elif request.GET.get('type') == 'recieved':
            queryset = PaymentRequest.objects.filter(recipient=request.user)
        else:
            queryset = PaymentRequest.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        

class PaymentRequestDetail(generics.GenericAPIView):
    serializer_class = PaymentRequestSerializer
    queryset = PaymentRequest.objects.all()
    def get(self, request, pk):
        paymentrequest = PaymentRequest.objects.get(uid=pk)
        serializer = self.get_serializer(paymentrequest)
        return Response(serializer.data)
    
    def patch(self, request, pk):
        paymentrequest = PaymentRequest.objects.get(uid=pk)
        user = request.user
        if paymentrequest.recipient != user:
            return Response({'message': 'unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        else:
            status = request.data['status']
            paymentrequest.status = status
            serializer = self.get_serializer(paymentrequest)
            return Response(serializer.data)
