import os
import time
from datetime import datetime

from poll_service import PollService
from common.db import CMSDataBase

POSTGRES_CONNECTION = {
    'host': 'postgres',
    'port': 5432,
    'dbname': 'cms',
    'user': 'cms_user',
    'password': os.environ['POSTGRES_CMS_USER_PASSWORD'],
}


def main():
    with CMSDataBase(config=POSTGRES_CONNECTION) as db:
        feeds = db.get_feeds_to_poll()

    poll_service = PollService()
    for feed in feeds:
        parsed = poll_service.poll(feed)

        if parsed is not None:
            with CMSDataBase(config=POSTGRES_CONNECTION) as db:
                db.update_feed_metadata(
                    feed_id=feed['id'],
                    last_modified=parsed['headers']['last-modified'],
                    etag=parsed['etag']
                )

                for entry in parsed.entries:
                    published_at_struct = entry.get('published_parsed')
                    if published_at_struct:
                        published_at = datetime.fromtimestamp(
                            time.mktime(published_at_struct)
                        )
                    else:
                        published_at = None
                    db.insert_article(
                        feed_id=feed['id'],
                        title=entry.get('title'),
                        link=entry.get('link'),
                        published_at=published_at,
                        content=entry.get('summary') or entry.get('content', [{}])[0].get('value')
                    )

if __name__ == '__main__':
    main()
