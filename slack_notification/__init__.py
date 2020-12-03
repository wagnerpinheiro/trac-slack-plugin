import pkg_resources

from slack_notification.ticket import *
from slack_notification.wiki import *

pkg_resources.require('Trac >= 1.0')

try:
    __version__ = __import__('pkg_resources').get_distribution('SlackNotificationPlugin').version
except (ImportError, pkg_resources.DistributionNotFound):
    pass
