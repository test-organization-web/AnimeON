from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from apps.user.serializers import UserSerializer
from rest_framework.response import Response
from apps.core.utils import swagger_auto_schema_wrapper
from apps.user.swager_views_docs import UserAPIViewDoc, UserAnimeCountAPIViewDoc
from apps.user.serializers import UserAnimeCountSerializer


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


class UserAnimeCountAPI(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserAnimeCountSerializer

    @swagger_auto_schema_wrapper(
        doc=UserAnimeCountAPIViewDoc,
        request_serializer_cls=None
    )
    def get(self, request, *args, **kwargs):
        user = self.get_object()
        count_viewed_anime = user.get_count_viewed_anime()
        data = {'count_viewed_anime': count_viewed_anime}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    def get_object(self):
        return self.request.user