from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from apps.user.serializers import UserSerializer, SettingsSerializer
from apps.core.utils import swagger_auto_schema_wrapper
from apps.user.swager_views_docs import UserAPIViewDoc
from apps.user.models import Settings
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView


class UserAPI(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    @swagger_auto_schema_wrapper(
        doc=UserAPIViewDoc,
        request_serializer_cls=None
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return self.request.user


class SettingsAPI(RetrieveAPIView):

    def get(self, request):
        settings = get_object_or_404(Settings, user=request.user)
        serializer = SettingsSerializer(settings)
        return Response(serializer.data)

    def post(self, request):
        settings = get_object_or_404(Settings, user=request.user)
        serializer = SettingsSerializer(settings, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
