from django.urls import path
from .views import WalletView, PaymentsView, WalletDetailView, TransactionHistory, Transactiondetail, PaymentDetail, TransferView, WalletBalance, DepositFunds, PaymentRequestView, PaymentRequestDetail

urlpatterns = [
    path('wallets/', WalletView.as_view(), name='wallets'),
    path('wallets/balance/', WalletBalance.as_view(), name='balance'),
    path('wallets/<int:pk>/', WalletDetailView.as_view(), name='wallet'),
    path('wallets/deposit/', DepositFunds.as_view(), name='deposit'),


    # wallet funding
    #path('wallets/top-up/', WalletView.as_view(), name='wallets'), 
    path('wallets/request/', PaymentRequestView.as_view(), name='requests'), 
    path('wallets/request/<str:pk>/', PaymentRequestDetail.as_view(), name='request') , 


    # wallet to wallet payment
    path('wallets/transfer/', TransferView.as_view(), name='payments'),
    #path('wallets/<str:username>/pay/', TransferView.as_view(), name='payments'),
    

    # Transactions Endpoints
    path('wallets/transactions/', TransactionHistory.as_view(), name='transactions'),
    path('wallets/transactions/<int:pk>/', Transactiondetail.as_view(), name='transaction'),


    # Payments Endpoints
    path('wallets/payments/history/', PaymentsView.as_view(), name='payments'),
    path('wallets/payments/<int:pk>/', PaymentDetail.as_view(), name='payment'),
]