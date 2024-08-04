class CommentMixin:
    def has_object_permission(self, obj):
        return True if obj.user.id == self.request.user.id else False
