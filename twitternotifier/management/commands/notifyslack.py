import sys
import slack

from django.core.management.base import BaseCommand

from twitternotifier.logging import get_logger
from twitternotifier.static_settings import STATIC_SETTINGS

logger = get_logger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        pass


def _to_notify(room, message, title='', author='', color='', icon_emoji=''):
    slack.api_token = STATIC_SETTINGS['SLACK_TOKEN']

    attachments = [{
        'title': title,
        'fallback': message,
        'color': color,
        'author_name': author,
        'icon_emoji': icon_emoji,
        'text': message,
        'html': ['text', 'pretext', 'title'],
    }]

    try:
        slack.chat.post_message(
            room, '', username=author, attachments=attachments, icon_emoji=icon_emoji)
    except slack.exception.NotAuthedError as err:
        logger.exception('[{}] {}'.format(
            sys._getframe().f_code.co_name, err))
