from django.db.models import Sum
from django.utils.timezone import datetime
from rest_framework import serializers

from .conf import settings
from .models import *
from base import helpers


class InvestSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    amount = serializers.FloatField()

    def validate(self, data):
        user = data['user']
        amount = data['amount']

        if amount < settings.ICO_MINIMUM_PURCHASE:
            raise serializers.ValidationError(
                f'You cannot invest less than {settings.ICO_MINIMUM_PURCHASE} USD')

        return data


class ICODetailSerializer(serializers.Serializer):
    stage = serializers.CharField()
    start = serializers.DateField()
    end = serializers.DateField()
    rates = serializers.DictField()
    bonus = serializers.FloatField()
    current_raised = serializers.FloatField()
    total_raised = serializers.FloatField()
    softcap = serializers.FloatField()
    hardcap = serializers.FloatField()
    is_ongoing = serializers.BooleanField()
    is_ended = serializers.BooleanField()


class ReferralSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        serializer_data = UserSerializer(value, context=self.context, many=True).data
        return serializer_data

    class Meta:
        model = User
        fields = ('email', 'referrals', 'date_joined')
        read_only_fields = ('email', 'referrals', 'date_joined')


class DirectReferralSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'date_joined')


class UserSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()
    num_of_referrals = serializers.SerializerMethodField()

    @classmethod
    def get_balance(self, obj):
        return helpers.get_token_balance(obj.address)

    @classmethod
    def get_num_of_referrals(self, obj):
        return obj.referrals.count()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'address', 
            'mobile_no', 'balance', 'num_of_referrals', 'affiliate_id', 
            'social_url', 'review', 'date_joined')
        read_only_fields = ('email', 'address')


class TransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transaction
        fields = ('id', 'code', 'amount', 'currency', 'description',
            'status', 'modified', 'created')
