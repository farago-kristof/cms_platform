import os
import time
from datetime import datetime

from poll_service import PollService
from common.db import CMSDataBase
from common.ustils import get_first_existing_value

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
            headers = parsed.headers
            last_modified = get_first_existing_value(d=headers, keys=('last_modified', 'last-modified'))
            with CMSDataBase(config=POSTGRES_CONNECTION) as db:
                db.update_feed_metadata(
                    feed_id=feed['id'],
                    last_modified=last_modified,
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
                    content = None
                    if 'content' in entry and isinstance(entry['content'], list) and entry['content']:
                        content = entry['content'][0].get('value')
                    if not content:
                        content = entry.get('summary')
                    db.insert_article(
                        feed_id=feed['id'],
                        title=entry.get('title'),
                        link=entry.get('link'),
                        published_at=published_at,
                        content=content
                    )

if __name__ == '__main__':
    main()
