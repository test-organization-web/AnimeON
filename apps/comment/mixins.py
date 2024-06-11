from django.core.exceptions import PermissionDenied


class CommentMixin:
    def has_object_permission(self, obj):
        return True if obj.user.id == self.request.user.id else False

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if self.has_object_permission(obj):
            return obj
        else:
            raise PermissionDenied("Access Denied : update or delete comment.")
