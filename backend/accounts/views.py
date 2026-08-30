from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from django.utils import timezone

from .match_service import determine_match
from .models import Match, User
from .serializers import (
    LoginSerializer,
    MatchCheckSerializer,
    MatchSerializer,
    SignupSerializer,
    UserSerializer,
)


def _tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
    }


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            first_error = next(iter(serializer.errors.values()))[0]
            return Response(
                {"detail": str(first_error)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = serializer.save()
        return Response(
            {"user": UserSerializer(user).data, **_tokens_for_user(user)},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data, context={"request": request}
        )
        if not serializer.is_valid():
            extra = serializer.errors.get("non_field_errors")
            if extra:
                return Response(
                    {"detail": extra[0]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        user = serializer.validated_data["user"]
        return Response(
            {"user": UserSerializer(user).data, **_tokens_for_user(user)}
        )


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class MatchListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        matches = Match.objects.filter(user=request.user)
        return Response(MatchSerializer(matches, many=True).data)

    def post(self, request):
        serializer = MatchSerializer(
            data=request.data, context={"request": request}
        )
        if not serializer.is_valid():
            first_error = next(iter(serializer.errors.values()))[0]
            return Response(
                {"detail": str(first_error)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        match = serializer.save()
        return Response(
            MatchSerializer(match).data, status=status.HTTP_201_CREATED
        )


class MatchCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MatchCheckSerializer(data=request.data)
        if not serializer.is_valid():
            first_error = next(iter(serializer.errors.values()))[0]
            return Response(
                {"detail": str(first_error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        boy_name = serializer.validated_data["boy_name"].strip()
        girl_name = serializer.validated_data["girl_name"].strip()

        result = determine_match(boy_name, girl_name)

        match = Match.objects.create(
            user=request.user,
            boy_name=boy_name,
            girl_name=girl_name,
            is_match=result["is_match"],
            checked_at=timezone.now(),
        )

        return Response(
            {
                "id": match.id,
                "boy_name": boy_name,
                "girl_name": girl_name,
                "is_match": result["is_match"],
                "message": result["message"],
                "checked_at": match.checked_at,
            },
            status=status.HTTP_201_CREATED,
        )
