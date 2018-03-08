import datetime
import time
import sys

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from twitternotifier.api.twitter import (
    twitterapi,
    TwitterTweet
)
from twitternotifier.logging import get_logger
from favorites.models import FavoriteTweet
from retweets.models import RetweetTweet

logger = get_logger(__name__)

GET_FAVORITE_REQUEST_LIMIT = 75  # requests / 15-min window
GET_RETWEET_REQUEST_LIMIT = 75  # requests / 15-min window
MIN_REQUEST = 15


class Command(BaseCommand):

    def handle(self, *args, **options):

        favorite_tweets = _get_favorites()
        _save_favorites(favorite_tweets)

        # retweet_tweets = _get_retweets()
        # _save_retweets(retweet_tweets)


def _get_favorites():

    logger.info('[{}] Get favorite tweets.'.format(
        sys._getframe().f_code.co_name))

    page = 0
    favorites = []
    while True:
        try:
            if page != 0 and page % GET_FAVORITE_REQUEST_LIMIT == 0:
                logger.info('[{}] Sleep {} sec.'.format(
                    sys._getframe().f_code.co_name, MIN_REQUEST * 60))
                time.sleep(MIN_REQUEST * 60)

            favs = twitterapi().favorites(
                id=twitterapi().me,
                page=page,
                tweet_mode='extended')
            if not favs:
                break

            favorites.extend(favs)
            time.sleep(2)

            page += 1

        except Exception as err:
            logger.exception('[{}] {}'.format(
                sys._getframe().f_code.co_name, err))
            break

    logger.info('[{}] Get {} favorite tweets.'.format(
        sys._getframe().f_code.co_name, len(favorites)))

    return [TwitterTweet(status) for status in favorites]


def _get_retweets():

    logger.info('[{}] Get retweet tweets.'.format(
        sys._getframe().f_code.co_name))

    page = 0
    retweets = []
    while True:
        try:
            if page != 0 and page % GET_RETWEET_REQUEST_LIMIT == 0:
                logger.info('[{}] Sleep {} sec.'.format(
                    sys._getframe().f_code.co_name, MIN_REQUEST * 60))
                time.sleep(MIN_REQUEST * 60)

            rets = twitterapi().retweets_of_me(
                id=twitterapi().me,
                page=page,
                tweet_mode='extended')
            if not rets:
                break

            retweets.extend(rets)
            time.sleep(2)
            page += 1

        except Exception as err:
            logger.exception('[{}] {}'.format(
                sys._getframe().f_code.co_name, err))
            break

    logger.info('[{}] Get {} retweet tweets.'.format(
        sys._getframe().f_code.co_name, len(retweets)))

    return [TwitterTweet(status) for status in retweets]


def _save_favorites(favorite_tweets):

    new_one = 0
    for tweet in favorite_tweets:
        try:
            favorite_tweet = FavoriteTweet(
                tweet_id=tweet.tweet_id,
                tweet=tweet.tweet,
                user_id=tweet.user_id,
                user_name=tweet.user_name,
                user_screen_name=tweet.user_screen_name,
                favorite_count=tweet.favorite_count,
                retweet_count=tweet.retweet_count,
                original_url=tweet.original_url)
            favorite_tweet.save()
            new_one += 1

        except IntegrityError as err:
            saved_tweet = FavoriteTweet.objects.get(
                tweet_id=tweet.tweet_id)
            saved_tweet.save()

    logger.info('[{}] {} new tweet saved.'.format(
        sys._getframe().f_code.co_name, new_one))


def _save_retweets(retweet_tweets):

    new_one = 0
    for tweet in retweet_tweets:
        try:
            retweet_tweet = RetweetTweet(
                tweet_id=tweet.tweet_id,
                tweet=tweet.tweet,
                user_id=tweet.user_id,
                user_name=tweet.user_name,
                user_screen_name=tweet.user_screen_name,
                favorite_count=tweet.favorite_count,
                retweet_count=tweet.retweet_count,
                original_url=tweet.original_url)
            retweet_tweet.save()
            new_one += 1

        except IntegrityError as err:
            saved_tweet = RetweetTweet.objects.get(
                tweet_id=tweet.tweet_id)
            saved_tweet.save()

    logger.info('[{}] {} new tweet saved.'.format(
        sys._getframe().f_code.co_name, new_one))
