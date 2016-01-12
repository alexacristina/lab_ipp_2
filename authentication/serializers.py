import datetime
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.forms import SetPasswordForm
from django.conf import settings

from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer
from rest_framework import serializers


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'last_login')
        write_only_fields = ('password',)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password1 = serializers.CharField()
    new_password2 = serializers.CharField()

    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = getattr(settings,
            'OLD_PASSWORD_FIELD_ENABLED', False
        )
        self.logout_on_password_change = getattr(settings,
            'LOGOUT_ON_PASSWORD_CHANGE', False
        )
        super(ChangePasswordSerializer, self).__init__(*args, **kwargs)

        if not self.old_password_field_enabled:
            self.fields.pop('old_password')
        print (self.context)
        self.request = self.context.get('request')
        print (self.request)
        self.user = getattr(self.request, 'user')
        # self.user = User.objects.get(username=username)
        print (self.user)

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password
        )
        if all(invalid_password_conditions):
            raise serializers.ValidationError('Invalid Password')
            return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(self.request, self.user)


    def patch(self, instance, validated_data):
        password = validated_data.get('password')
        new_password_data = validated_data.pop('new_password')
        confirm_password_data = validated_data.pop('confirm_password')
        return instance


class GroupSerializer(Serializer):

    class Meta:
        model = Group

