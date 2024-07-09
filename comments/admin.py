from django.contrib import admin
from comments.models import Comment
# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment_by', 'post', 'post_onwer']

    def post_onwer(self,obj):
        return f"{obj.post.account.user.first_name} {obj.post.account.user.last_name}"
    
    def post(self, obj):
        return f"{obj.post.image}"
    
    def comment_by(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    
admin.site.register(Comment, CommentAdmin)
