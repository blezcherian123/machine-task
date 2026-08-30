from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from rest_framework import serializers

from .models import Match, User


letters_validator = RegexValidator(
    regex=r"^[A-Za-z ]+$",
    message="Only letters and spaces are allowed.",
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "tenant_name", "date_joined"]


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "email", "password", "full_name", "tenant_name"]
        extra_kwargs = {
            "email": {"required": True},
            "full_name": {"required": False, "allow_blank": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get("email", "").lower()
        password = attrs.get("password")
        user = authenticate(request=self.context.get("request"), email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        if not user.is_active:
            raise serializers.ValidationError("This account is disabled")
        attrs["user"] = user
        return attrs


class MatchSerializer(serializers.ModelSerializer):
    boy_name = serializers.CharField(validators=[letters_validator])
    girl_name = serializers.CharField(validators=[letters_validator])

    class Meta:
        model = Match
        fields = [
            "id",
            "boy_name",
            "girl_name",
            "is_match",
            "match_percentage",
            "checked_at",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "is_match",
            "match_percentage",
            "checked_at",
            "created_at",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request else None
        return Match.objects.create(user=user, **validated_data)


class MatchCheckSerializer(serializers.Serializer):
    boy_name = serializers.CharField(validators=[letters_validator])
    girl_name = serializers.CharField(validators=[letters_validator])
