from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.user')
    title = models.CharField(max_length=256)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments.filter(is_approved=True)

    def __str__(self):
        return self.title

class Heart(models.Model):
    post = models.ForeignKey('blog.Post', related_name='hearts')
    lover = models.ForeignKey('auth.user')
    

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    #author = models.CharField(max_length=128)
    author = models.ForeignKey('auth.user')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)

    def approve(self):
        self.is_approved = True
        self.save()

    def __str__(self):
        return self.text
