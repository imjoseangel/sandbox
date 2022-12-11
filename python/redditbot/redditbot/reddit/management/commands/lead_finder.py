# Inside redditbot/redditbot/reddit/management/commands/lead_finder.py file
import datetime as DT
import re

import praw
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.timezone import make_aware

from redditbot.reddit.models import Lead

KEYWORD = "facebook"
SUBREDDIT = 'marketing'

reddit = praw.Reddit(
    client_id=settings.REDDIT_CLIENT_ID,
    client_secret=settings.REDDIT_SECRET,
    user_agent=settings.REDDIT_USERAGENT,
)


def convert_to_ts(unix_time):
    try:
        ts = make_aware(DT.datetime.fromtimestamp(unix_time))
        return ts
    except:
        print(f"Converting utc failed for {unix_time}")
        return None


def populate_lead(keyword, subreddit):
    for submission in reddit.subreddit(subreddit).hot(limit=100):
        if re.search(keyword, submission.title, re.IGNORECASE):
            if not Lead.objects.filter(post_id=submission.id):
                Lead.objects.create(post_id=submission.id,
                                    title=submission.title,
                                    url=submission.permalink,
                                    content=submission.selftext,
                                    posted_at=convert_to_ts(submission.created_utc))


class Command(BaseCommand):
    help = 'Populating leads'

    def handle(self, *args, **kwargs):
        try:
            current_time = timezone.now()
            self.stdout.write(f'Populating leads at {(current_time)}')
            populate_lead(KEYWORD, SUBREDDIT)
        except BaseException as e:
            current_time = timezone.now().strftime('%X')
            self.stdout.write(self.style.ERROR(f'Populating feeds failed at {current_time} because {str(e)}'))

        current_time = timezone.now()
        self.stdout.write(self.style.SUCCESS(f'Successfully populated new leads at {current_time}'))
        return
