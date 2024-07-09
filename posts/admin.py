from django.contrib import admin
from . import models
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['post_owner','description', 'image']

    def post_owner(self, obj):
        return f"{obj.account.user.first_name} {obj.account.user.last_name}"
    
# class LikeAdmin(admin.ModelAdmin):
#     list_display = ['post_owner', 'post_image', 'like_by']

#     def post_onwer(self,obj):
#         return f"{obj.post.account.user.first_name} {obj.post.account.user.last_name}"
    
#     def post_image(self, obj):
#         return f"{obj.post.image}"
    
#     def like_by(self, obj):
#         return f"{obj.user.first_name} {obj.user.last_name}"
    
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Like)

