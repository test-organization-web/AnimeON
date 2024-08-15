from rest_framework import serializers

from apps.comment.models import Comment, Reaction


class CreateCommentSerializer(serializers.ModelSerializer):
    parent_id = serializers.IntegerField(required=False)

    class Meta:
        model = Comment
        fields = ('content', 'object_id', 'parent_id')


class CommentReactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('reaction',)


class ResponseCommentReactSerializer(serializers.Serializer):
    action = serializers.ChoiceField(
        choices=(('DELETE', 'DELETE'), ('CHANGE', 'CHANGE'), ('NEW', 'NEW'))
    )
