from django.contrib.contenttypes.models import ContentType
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.comment.mixins import CommentMixin
from apps.comment.models import Comment, Reaction
from apps.comment.serializers import (
    CreateCommentSerializer, CommentReactSerializer
)
from apps.comment.swagger_views_docs import (
    CommentCreateAPIViewDoc, CommentReactAPIViewDoc
)
from apps.comment.swagger_views_docs import ReplyCommentAPIViewDoc
from apps.comment.paginators import CommentAnimeListPaginator
from apps.anime.serializers import ResponseCommentAnimeSerializer
from apps.core.utils import swagger_auto_schema_wrapper
from apps.core.utils import validate_request_data


class CommentCreateAPIView(CommentMixin, APIView):
    permission_classes = (IsAuthenticated,)
    request_serializer = CreateCommentSerializer
    response_serializer = ResponseCommentAnimeSerializer

    @swagger_auto_schema_wrapper(
        doc=CommentCreateAPIViewDoc,
        operation_id='create_anime_comment',
        request_serializer_cls=request_serializer
    )
    @validate_request_data(serializer_cls=request_serializer)
    def post(self, request, serializer: CreateCommentSerializer, *args, **kwargs):
        serializer.validated_data['user_id'] = self.request.user.id
        serializer.validated_data['content_main'] = serializer.validated_data['content']
        app_name = 'anime'
        model_name = 'anime'
        serializer.validated_data['content_type'] = ContentType.objects.get(
            app_label=app_name, model=model_name.lower())
        comment: Comment = serializer.save()
        response_ser = self.response_serializer(comment).data
        return Response(data=response_ser, status=status.HTTP_201_CREATED)


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
                return Response(data={'action': 'DELETE'}, status=status.HTTP_200_OK)
            else:  # Change Previous Reaction
                reaction.react = user_reaction
                reaction.save()
                return Response(data={'action': 'CHANGE'}, status=status.HTTP_200_OK)
        else:  # Create New Reaction
            serializer.save()
        return Response(data={'action': 'NEW'}, status=status.HTTP_200_OK)


class ReplyCommentAPIView(ListAPIView):
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

    permission_classes = (IsAuthenticated,)  # Or anon users can't register

    serializer_class = ResponseCommentAnimeSerializer
    pagination_class = CommentAnimeListPaginator

    @swagger_auto_schema_wrapper(
        doc=ReplyCommentAPIViewDoc,
        operation_id='get_reply_comments',
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        # Views have behaviour which varies dynamically based on request parameters
        # (using self.kwargs in their get_queryset, get_serializer, etc methods).
        # drf-yasg is unable to handle this because no requests are actually made to the inspected views.
        if getattr(self, "swagger_fake_view", False):
            # It means that the view instance was artificially created as part of a swagger schema request.
            return Comment.objects.none()

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        content_type = ContentType.objects.get(app_label='anime', model='anime')
        queryset = Comment.objects.filter(
            content_type=content_type, parent_id=self.kwargs[lookup_url_kwarg]
        )
        return queryset.order_pinned_newest()
