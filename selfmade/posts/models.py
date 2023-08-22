from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.utils import timezone
from users.models import MyUser

class Post(models.Model):
    title = models.CharField(max_length=175)
    content = RichTextUploadingField()
    description = models.CharField(max_length=325)
    image = models.ImageField(upload_to="post_images/")
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    tags = TaggableManager()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.title
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='user_name')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_date']

    def __str__(self) -> str:
        return self.text
    

class Vote(models.Model):
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class CommentVote(models.Model):
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    direction = models.IntegerField()