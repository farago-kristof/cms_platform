import os

from poll_service import PollService
from common.db import CMSDataBase

POSTGRES_CONNECTION = {
    'host': 'postgres',
    'port': 5432,
    'dbname': 'cms',
    'user': 'cms_user',
    'password': os.environ['POSTGRES_CMS_USER_PASSWORD'],
}

if __name__ == '__main__':

    with CMSDataBase(config=POSTGRES_CONNECTION) as db:
        feeds = db.get_feeds_to_poll()

    poll_service = PollService()
    for feed in feeds:
        result = poll_service.poll(feed)
        if result is not None:
            with CMSDataBase(config=POSTGRES_CONNECTION) as db:
                db.update_feed_metadata(
                    feed_id=feed['id'],
                    last_modified=result['headers']['last-modified'],
                    etag=result['etag']
                )
