import random
import sys
import time

import slack
import slack.chat

from django.core.management.base import BaseCommand

from twitternotifier.logging import get_logger
from twitternotifier.static_settings import STATIC_SETTINGS
from favorites.models import FavoriteTweet

logger = get_logger(__name__)

NUM_OF_NOTIFY = 10


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            entries = FavoriteTweet.objects.order_by('?')[:NUM_OF_NOTIFY]

            for entry in entries:
                _to_notify(room=STATIC_SETTINGS['SLACK_NOTIFICATION_ROOM_ID'],
                           message=entry.original_url,
                           icon_emoji=':heart:')
                time.sleep(5)
        except Exception as err:
            logger.exception('[{}] {}'.format(
                sys._getframe().f_code.co_name, err))


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
