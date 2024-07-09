from django.db import models
from posts.models import Post
from django.contrib.auth.models import User

# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"comment by : {self.user.first_name}"
