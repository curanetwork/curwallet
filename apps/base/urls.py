"""urlconf for the base application"""

from django.urls import path, include
from rest_framework import routers

from base import views


router = routers.DefaultRouter()
router.register(r'transactions', views.TransactionViewSet, 'transaction')
router.register(r'referrals', views.DirectReferralViewSet, 'referral')

urlpatterns = [
  path('appi/', include(router.urls)),
  path('appi/invest/', views.invest),
  path('appi/details/', views.details),
  path('appi/ipn/', views.ipn)
]