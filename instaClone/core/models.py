from django.db import models
from django.contrib.auth.models import User, UserManager
import uuid

User._meta.get_field('email')._unique = True


class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=150, blank=True, null=True)
    working_at = models.CharField(max_length=150, default='#', blank=True, null=True)
    profileimg = models.ImageField(upload_to='profile_imgs',default='blank_profile.jpg')

    objects = UserManager() 

    def __str__(self):
         return self.user.username


class UserFollowing(models.Model):
    user_id = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'following_user_id'], name='unique_followers' )
        ]
        unique_together = (('user_id', 'following_user_id'),)

        ordering = ['created']

        def __str__(self):
            return f"{self.user_id} follows {self.following_user_id}" 
    

class PostModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    post_img = models.ImageField(upload_to='post_imgs')
    post_caption = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)
    post_owner = models.ForeignKey(User, related_name='poster', on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name='like', blank=True, through='LikeModel')

    def __str__(self):
        return f'{self.post_owner} uploaded new photo a {self.post_date}'
    
    class Meta:
        ordering = ('-post_date',)

class LikeModel(models.Model):
    like_owner = models.ForeignKey(User, related_name='liker', on_delete=models.CASCADE, default='1')
    liked_post = models.ForeignKey(PostModel, related_name='liked', on_delete=models.CASCADE, default=1)
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.like_owner} liked {self.liked_post.post_owner}'s photo at {self.liked_at}"
    
    class Meta:
        ordering = ("-liked_at",)