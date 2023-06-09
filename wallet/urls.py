from django.urls import path
from .views import WalletView, WalletDetailView, TransactionHistory, Transactiondetail, TransferView, WalletBalance, DepositFunds, PaymentRequestView, PaymentRequestDetail, PaymentLinkView, PaywithLinkView

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
    path('wallets/pay/<str:id>/', PaywithLinkView.as_view(), name='pay'),
    

    # Transactions Endpoints
    path('wallets/transactions/', TransactionHistory.as_view(), name='transactions'),
    path('wallets/transactions/<int:pk>/', Transactiondetail.as_view(), name='transaction'),


    # Payments Endpoints
    path('wallets/links/', PaymentLinkView.as_view(), name='paym'),
]
