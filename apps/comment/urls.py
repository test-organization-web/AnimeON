from django.urls import path
from apps.comment.views import CommentCreateAPIView, CommentReactAPIView, ReplyCommentAPIView

app_name = 'comment'

urlpatterns = [
    path('', CommentCreateAPIView.as_view(), name='anime_comment'),
    path('<int:pk>/reaction/', CommentReactAPIView.as_view(), name='reaction_comment'),
    path('<int:pk>/reply/', ReplyCommentAPIView.as_view(), name='get_reply_comments'),
]
