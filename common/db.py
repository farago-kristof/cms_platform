import psycopg2
from psycopg2.extras import RealDictCursor

from common.mixins import LoggerMixin


class CMSDataBase(LoggerMixin):
    """Handles PostgreSQL database operations for feed polling"""

    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        self.conn = None

    def __enter__(self):
        self.conn = psycopg2.connect(**self.config)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def get_feeds_to_poll(self):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM feeds.rss_feed
                ORDER BY last_polled NULLS FIRST
            """)
            results = cur.fetchall()
            self.logger.debug("Fetched %d feeds", len(results))
            return results

    def update_feed_metadata(self, feed_id, etag, last_modified):
        self.logger.debug("Updating feed metadata, feed_id=%s, etag=%s, last_modified=%s", feed_id, etag, last_modified)
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE feeds.rss_feed
                SET last_polled = now(),
                    etag = %s,
                    last_modified = %s
                WHERE id = %s
            """, (etag, last_modified, feed_id))
        self.conn.commit()

    def insert_article(self, feed_id, title, link, published_at=None, content=None):
        self.logger.debug(
            "Inserting article: feed_id=%s, title=%s, link=%s", feed_id, title, link
        )
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO feeds.articles (feed_id, title, link, published_at, content)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (link) DO NOTHING
            """, (feed_id, title, link, published_at, content))
        self.conn.commit()
