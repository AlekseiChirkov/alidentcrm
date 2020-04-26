from rest_framework import serializers
from django.contrib.auth import authenticate


from .models import MyUser


class ChoiceField(serializers.Field):
    def __init__(self, choices, **kwargs):
        self._choices = choices
        super(ChoiceField, self).__init__(**kwargs)

    def to_representation(self, obj):
        return self._choices[obj]

    def to_internal_value(self, data):
        return getattr(self._choices, data)


class MyUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    category = serializers.ChoiceField(choices=MyUser.USER_TYPES)
    token = serializers.CharField(max_length=256, read_only=True)

    class Meta:
        model = MyUser
        fields = [
            'id', 'username', 'email', 'password', 'password2',
            'name', 'surname', 'patronymic', 'birthday', 'category', 'token']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        account = MyUser(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            name=self.validated_data['name'],
            surname=self.validated_data['surname'],
            patronymic=self.validated_data['patronymic'],
            birthday=self.validated_data['birthday'],
            category=self.validated_data['category'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match'})
        account.set_password(password)
        account.save()
        return account


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=64, write_only=True)
    token = serializers.CharField(max_length=256, read_only=True)
    is_staff = serializers.BooleanField(read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        if username is None:
            raise serializers.ValidationError('Username is required')
        if password is None:
            raise serializers.ValidationError('Password is required')
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError('User with this username or '
                                              'password does not exist')
        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated')

        return {
            'username': user.username,
            'token': user.token,
            'is_staff': user.is_staff
        }
