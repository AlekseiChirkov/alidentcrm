from rest_framework import serializers

from .models import MyUser, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MyUserSerializer(serializers.ModelSerializer):
    # RoleSerializer(many=True)
    # role = serializers.StringRelatedField(many=False)

    class Meta:
        model = MyUser
        fields = '__all__'
