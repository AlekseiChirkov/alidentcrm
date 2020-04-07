from rest_framework import serializers

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

    class Meta:
        model = MyUser
        fields = ['id', 'username', 'email', 'password', 'password2', 'name', 'surname', 'patronymic', 'birthday', 'category']
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
