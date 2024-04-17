from rest_framework import permissions
from rest_framework.generics import RetrieveAPIView
from apps.user.serializers import UserSerializer

from apps.core.utils import swagger_auto_schema_wrapper
from apps.user.swager_views_docs import UserAPIViewDoc


class UserAPI(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    @swagger_auto_schema_wrapper(
        doc=UserAPIViewDoc,
        request_serializer_cls=None
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return self.request.user
