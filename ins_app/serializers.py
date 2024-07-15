from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, PolicyDetail
from datetime import datetime


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user',
            'dob',
            'gender',
            'mobile',
            'full_name'
        ]

    def validate_dob(self, dob):
        today = datetime.now()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 23:
            raise serializers.ValidationError('Age should be greater than or equal to 23')
        elif age > 56:
            raise serializers.ValidationError('Age should be less than or equal to 56')
        return dob


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User(username=validated_data.get('username'))
        user.set_password(validated_data.get('password'))
        user.save()
        return user
    

class PolicySerializer(serializers.ModelSerializer):
    profile_details = ProfileSerializer(source='profile', read_only=True)

    class Meta:
        model = PolicyDetail
        fields = '__all__'
        extra_fields = ['profile_details']

    def validate(self, data):
        ppt = data.get('ptt')
        pt = data.get('pt')
        premium = data.get('premium')
        sum_assured = data.get('sum_assured')
        min_sum_assured = premium * 10

        if ppt < 5:
            raise serializers.ValidationError('PPT should be greater than or equal to 5')
        elif ppt > 10:
            raise serializers.ValidationError('PPT should be less than or equal to 10')
        if pt < 10:
            raise serializers.ValidationError('PT should be greater than or equal to 10')
        elif pt > 20:
            raise serializers.ValidationError('PT should be less than or equal to 20')
        if pt < ppt:
            raise serializers.ValidationError('PT should be always greater than PPT')
        if premium < 10000:
            raise serializers.ValidationError('Premium should be greater than or equal to 10000')
        elif premium > 50000:
            raise serializers.ValidationError('Premium should be less than or equal to 50000')
        if sum_assured < min_sum_assured:
            raise serializers.ValidationError('Sum assured should be minimum 10 times the Premium')
        elif sum_assured > 5000000:
            raise serializers.ValidationError('Sum assured should not be greater than 5000000')

        return data
    