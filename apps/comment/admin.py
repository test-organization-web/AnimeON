from django.contrib import admin

from apps.comment.models import Comment


class ListFilterByParent(admin.SimpleListFilter):
    title = 'parent'
    parameter_name = 'parent'

    def lookups(self, request, model_admin):
        return (
            ('parent', 'Comments'), ('child', 'Replies')
        )

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == 'parent':
                return queryset.filter(parent__isnull=True)
            elif self.value() == 'child':
                return queryset.filter(parent__isnull=False)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'content', 'user', 'content_object', 'created', 'updated')
    search_fields = ('content',)
    list_filter = (ListFilterByParent,)
    readonly_fields = ('user', 'content_main', 'content', 'parent', 'content_type',
                       'content_object', 'object_id', 'urlhash', 'created',)
