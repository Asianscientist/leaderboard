from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from .models import GamesModel
from django.utils import timezone
User=get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[
        RegexValidator(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")],
                                     style={'input_type': 'password', 'placeholder': 'Password'})
    password2 = serializers.CharField(write_only=True, required=True,
                                      style={'input_type': 'password', 'placeholder': 'Password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'is_staff')
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'is_staff': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_staff=validated_data['is_staff']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
        read_only_fields = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])

        if not user:
            raise serializers.ValidationError('Incorrect username or password.')

        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')

        return {'user': user}

class GameSerializerModel(serializers.ModelSerializer):
        class Meta:
            model=GamesModel
            fields="__all__"
        
        
class SubmissionSerializer(serializers.Serializer):
    game_name=serializers.CharField(max_length=100)
    submission_date = serializers.DateTimeField(default=timezone.now)
    score=serializers.IntegerField()
    submission_data=serializers.CharField()
    # def 