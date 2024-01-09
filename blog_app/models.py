from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField
from .helpers import *
# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    token = models.CharField(max_length=100)



class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = FroalaField()
    slug  = models.SlugField(max_length=1000 , null=True , blank =True)
    image = models.ImageField(upload_to='blog')
    user = models.ForeignKey(User,blank = True, null = True,on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)



    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(Blog, self).save(*args, **kwargs)