import datetime
import tweepy

from twitternotifier.static_settings import STATIC_SETTINGS


class TwitterAPI:
    """
    Class for performing lazy loading of tweepy.API
    """

    def __init__(self):
        self._api = None

    def __call__(self, *args, **kwargs):
        if not isinstance(self._api, tweepy.API):
            auth = tweepy.OAuthHandler(
                consumer_key=STATIC_SETTINGS['TWITTER_CONSUMER_KEY'],
                consumer_secret=STATIC_SETTINGS['TWITTER_CONSUMER_SECRET'])
            auth.set_access_token(
                STATIC_SETTINGS['TWITTER_ACCESS_TOKEN'],
                STATIC_SETTINGS['TWITTER_ACCESS_SECRET'])

            self._api = tweepy.API(auth)

        return self._api


twitterapi = TwitterAPI()


class TwitterTweet:

    def __init__(self, status):
        self._status = status

    @property
    def tweet_id(self):
        return str(self._status.__dict__.get('id', ''))

    @property
    def tweet(self):
        return self._status.__dict__.get('full_text', '')

    @property
    def user_id(self):
        user = self._status.__dict__.get('user')
        return str(user.__dict__.get('id', '')) if user else ''

    @property
    def user_name(self):
        user = self._status.__dict__.get('user')
        return str(user.__dict__.get('name', '')) if user else ''

    @property
    def user_screen_name(self):
        user = self._status.__dict__.get('user')
        return str(user.__dict__.get('screen_name', '')) if user else ''

    @property
    def published_at(self):
        return self._status.__dict__.get('created_at', datetime.datetime.fromtimestamp(0)) \
                                    .replace(tzinfo=datetime.timezone.utc) \
                                    .astimezone(datetime.timezone(datetime.timedelta(hours=+9), 'JST')) \
                                    .replace(tzinfo=datetime.timezone.utc)

    @property
    def favorite_count(self):
        return self._status.__dict__.get('favorite_count', 0)

    @property
    def retweet_count(self):
        return self._status.__dict__.get('retweet_count', 0)

    @property
    def original_url(self):
        return 'https://twitter.com/{}/status/{}'.format(self.user_screen_name, self.tweet_id)
