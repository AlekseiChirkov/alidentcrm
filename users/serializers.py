from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import MyUser, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MyUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password', 'password2', 'name', 'surname', 'patronymic', 'birthday']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        account = MyUser(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match'})
        account.set_password(password)
        account.save()
        return account

    # password = serializers.CharField(
    #     write_only=True,
    #     required=True,
    #     style={'input_type': 'password'}
    # )
    # password2 = serializers.CharField(
    #     label='Confirm Password',
    #     style={'input_type': 'Password'}
    # )
    #
    # class Meta:
    #     model = MyUser
    #     fields = ['username', 'email', 'password', 'password2']
    #     extra_kwargs = {
    #         'password': {'write_only': True},
    #         'password2': {'write_only': True},
    #     }
    #
    # def validate(self, data):
    #     password = data.get('password')
    #     confirm_password = data.pop('password2')
    #     if password != confirm_password:
    #         raise ValidationError('Пароли не совпадают')
    #     return data
    #
    # def create(self, validated_data):
    #     user = MyUser(
    #         email=validated_data['email'],
    #         username=validated_data['username'],
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user
