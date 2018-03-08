from django.db import models
from django.utils import timezone

from twitternotifier.api.twitter import twitterapi

# Create your models here.


class FavoriteTweet(models.Model):

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
    original_url = models.CharField(max_length=255)

    def __str__(self):
        return '[@{}] {}...'.format(
            self.user_screen_name,
            self.tweet[:80].replace('\n', ''))

    def delete(self, *args, **kwargs):
        twitterapi().destroy_favorite(int(self.tweet_id))
        return super(FavoriteTweet, self).delete(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'twitter_favorites'
