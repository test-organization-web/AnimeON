from django.contrib.contenttypes.models import ContentType
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.comment.mixins import CommentMixin
from apps.comment.models import Comment, Reaction
from apps.comment.serializers import (
    CreateCommentSerializer, CommentReactSerializer
)
from apps.comment.swagger_views_docs import (
    CommentCreateAPIViewDoc, CommentReactAPIViewDoc
)
from apps.core.utils import swagger_auto_schema_wrapper
from apps.core.utils import validate_request_data


class CommentCreateAPIView(CommentMixin, CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateCommentSerializer

    @swagger_auto_schema_wrapper(
        doc=CommentCreateAPIViewDoc,
        operation_id='create_anime_comment',
    )
    @validate_request_data(serializer_cls=serializer_class)
    def post(self, request, serializer: CreateCommentSerializer, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.validated_data['user_id'] = self.request.user.id
        serializer.validated_data['content_main'] = serializer.validated_data['content']
        app_name = 'anime'
        model_name = 'anime'
        serializer.validated_data['content_type'] = ContentType.objects.get(
            app_label=app_name, model=model_name.lower())

        super().perform_create(serializer)


class CommentDelete(CommentMixin, GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, urlhash, *args, **kwargs):
        comment = Comment.objects.get(urlhash=urlhash)
        if comment:
            comment.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CommentReactAPIView(CommentMixin, GenericAPIView):
    lookup_url_kwarg = 'pk'
    lookup_field = 'pk'
    queryset = Comment.objects.all()

    permission_classes = (IsAuthenticated,)
    serializer_class = CommentReactSerializer

    @swagger_auto_schema_wrapper(
        doc=CommentReactAPIViewDoc,
        operation_id='reaction_comment',
    )
    @validate_request_data(serializer_cls=serializer_class)
    def post(self, request, serializer: CommentReactSerializer, *args, **kwargs):
        comment = self.get_object()
        serializer.validated_data['comment_id'] = comment.id
        serializer.validated_data['user_id'] = request.user.id
        user_reaction = serializer.validated_data['reaction']

        reaction = Reaction.objects.filter(user=request.user.id, comment_id=comment.id).first()

        if reaction:  # Update Previous Reaction
            if reaction.reaction == user_reaction:  # Delete Previous Reaction
                reaction.delete()
            else:  # Change Previous Reaction
                reaction.react = user_reaction
                reaction.save()
        else:  # Create New Reaction
            serializer.save()

        return Response(status=status.HTTP_200_OK)
