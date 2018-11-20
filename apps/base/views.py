import json
from django.db.models import Sum
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from coinbase_commerce.client import Client
from coinbase_commerce.webhook import Webhook
from base import helpers
from .conf import settings
from .models import *
from .serializers import *


# REST API VIEWS


@api_view(['POST'])
def ipn(request):
    """
    Webhook handling for Coinbase Commerce
    """

    if request.method == 'POST':
        request_sig = request.META.get('HTTP_X_CC_WEBHOOK_SIGNATURE', None)
        
        '''
        # this was done in flask = request.data.decode('utf-8')
        try:
            # signature verification and event object construction
            event = Webhook.construct_event(
                json.dumps(request.data), request_sig, settings.ICO_COINBASE_WEBHOOK_SECRET)
        except Exception as e:
            return Response(
                {'message': 'Signature verification failed'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        '''
        event = request.data['event']
        user = User.objects.get(pk=event['data']['metadata']['user_id'])
        code = event['data']['code']
        amount = float(event['data']['local']['amount'])
        purchased = helpers.calculate_bought(amount)
        status = event['type'].split(':')[1]

        if status == 'pending':
            Transaction.objects.create(
                user=user,
                code=code,
                amount=amount,
                currency='USD',
                description=f'[{settings.ICO_STAGE}] Purchased {purchased} {settings.ICO_TOKEN_SYMBOL.upper()}',
                status=status
            )
        elif status == 'confirmed':
            tx = Transaction.objects.get(user=user, code=code)
            tx.status = status
            tx.save()

            Transaction.objects.create(
                user=user,
                code=helpers.transfer_tokens(user, purchased),
                amount=purchased,
                currency=settings.ICO_TOKEN_SYMBOL.upper(),
                description=f'[{settings.ICO_STAGE}] Received {purchased} {settings.ICO_TOKEN_SYMBOL.upper()}',
                status=status
            )

        return Response({'message': 'success'}, status=status.HTTP_200_OK)
        

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def invest(request):
    """
    Purchase token
    """

    if request.method == 'POST':
        serializer = InvestSerializer(
            data=request.data,
            context={'request': request}
        )

        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        client = Client(api_key=settings.ICO_COINBASE_API_KEY)
        
        try:
            charge = client.charge.create(
                name=f'{settings.ICO_TOKEN_NAME} Purchase',
                description='ICO participation',
                local_price={
                    'amount': request.data['amount'],
                    'currency': 'USD'
                },
                pricing_type='fixed_price',
                metadata={ 'user_id': request.user.id }
            )
        except Exception as e:
            return Response(
                {'message': 'Too many requests at this time. Please try again'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        return Response({'checkout_url': charge.hosted_url}, status=status.HTTP_200_OK)


@api_view(['GET'])
def details(request):
    """
    Return details of ICO
    """

    current_raised = Transaction.objects.filter(
        currency='USD',
        status='confirmed',
        description__contains=settings.ICO_STAGE
    ).aggregate(raised=Sum('amount'))['raised'] or 0.0

    total_raised = Transaction.objects.filter(
        currency='USD',
        status='confirmed'
    ).aggregate(raised=Sum('amount'))['raised'] or 0.0

    currencies = list()

    for currency in settings.ICO_CURRENCIES:
        currencies = currencies + [currency[0].upper()]

    if request.method == 'GET':
        serializer = ICODetailSerializer(data={
            'token_name': settings.ICO_TOKEN_NAME,
            'token_symbol': settings.ICO_TOKEN_SYMBOL,
            'stage': settings.ICO_STAGE,
            'start': settings.ICO_START,
            'end': settings.ICO_END,
            'price': settings.ICO_PRICE,
            'currencies': currencies,
            'bonus': settings.ICO_BONUS,
            'current_raised': current_raised,
            'total_raised': total_raised,
            'softcap': settings.ICO_SOFTCAP,
            'hardcap': settings.ICO_HARDCAP,
            'is_ongoing': helpers.is_ongoing(),
            'is_ended': helpers.is_ended()
        })

        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows transactions to be viewed.
    """
    serializer_class = TransactionSerializer
    http_method_names = ['get', 'head']
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Transaction.objects.filter(user__id=self.request.user.id).order_by('-modified')


class DirectReferralViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows referrals to be viewed.
    """
    serializer_class = DirectReferralSerializer
    http_method_names = ['get', 'head']
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.referrals


class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows faqs to be viewed.
    """
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    http_method_names = ['get', 'head']
