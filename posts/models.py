from django.db import models
from accounts.models import Account
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    account = models.ForeignKey(Account, on_delete= models.CASCADE)
    image = models.ImageField(upload_to='posts/images/', null=True, blank=True)
    description = models.TextField()
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.image}"
    

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"post_owner: {self.post.account.user.first_name} , react_user: {self.user.first_name}"



