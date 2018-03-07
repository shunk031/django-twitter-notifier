from django.db import models
from django.utils import timezone
# Create your models here.


class RetweetTweet(models.Model):

    id = models.BigAutoField(primary_key=True)
    tweet_id = models.CharField(max_length=255, unique=True)
    tweet = models.CharField(max_length=300)
    user_id = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    user_screen_name = models.CharField(max_length=255)
    update_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)
    favorite_count = models.IntegerField(default=0)
    retweet_count = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'twitter_retweets'
