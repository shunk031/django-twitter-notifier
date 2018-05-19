import random
import sys
import time

import slack
import slack.chat
import tweepy

from django.core.management.base import BaseCommand

from twitternotifier.api.twitter import twitterapi
from twitternotifier.logging import get_logger
from twitternotifier.static_settings import STATIC_SETTINGS
from favorites.models import FavoriteTweet

logger = get_logger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            entries = FavoriteTweet.objects.order_by('?')[:STATIC_SETTINGS['NUM_OF_NOTIFY']]
            while True:
                entries = _remove_protected_user_entry(entries)
                entries = _remove_deleted_tweets(entries)
                entries = list(set(entries))  # remove duplicates

                if len(entries) >= STATIC_SETTINGS['NUM_OF_NOTIFY']:
                    break

                entries += FavoriteTweet.objects.order_by('?')[:STATIC_SETTINGS['NUM_OF_NOTIFY'] - len(entries)]

            for entry in entries:
                _to_notify(room=STATIC_SETTINGS['SLACK_NOTIFICATION_ROOM_ID'],
                           message=entry.original_url,
                           icon_emoji=':heart:')
                time.sleep(5)
        except Exception as err:
            logger.exception('[{}] {}'.format(
                sys._getframe().f_code.co_name, err))


def _remove_protected_user_entry(entries):

    new_entries = []
    for entry in entries:
        try:
            is_protected = twitterapi().get_user(entry.user_id).protected

            if not is_protected:
                new_entries.append(entry)
        except tweepy.error.TweepError as err:
            logger.exception('[{}] {}'.format(
                sys._getframe().f_code.co_name, err))

    return new_entries


def _remove_deleted_tweets(entries):

    entry_ids = [entry.tweet_id for entry in entries]
    lookup_result = twitterapi().statuses_lookup(entry_ids)
    lookup_entry_ids = set([result.id_str for result in lookup_result])

    new_entries = []
    for entry in entries:
        if entry.tweet_id in lookup_entry_ids:
            new_entries.append(entry)

    return new_entries


def _to_notify(room, message, icon_emoji=''):
    slack.api_token = STATIC_SETTINGS['SLACK_TOKEN']

    try:
        slack.chat.post_message(
            room,
            message,
            username='Favorite Notification Man',
            icon_emoji=icon_emoji)

    except slack.exception.NotAuthedError as err:
        logger.exception('[{}] {}'.format(
            sys._getframe().f_code.co_name, err))
