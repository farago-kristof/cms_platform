import psycopg2
from psycopg2.extras import RealDictCursor
from redis import Redis
from rq import Queue

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
                        SELECT *
                        FROM feeds.rss_feed
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
                        SET last_polled   = now(),
                            etag          = %s,
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
                        VALUES (%s, %s, %s, %s, %s) ON CONFLICT (link) DO NOTHING
                        RETURNING id;
                        """, (feed_id, title, link, published_at, content))
            inserted_id = cur.fetchone()[0]
            self.conn.commit()
            return inserted_id

    def get_article_by_id(self, article_id):
        """Fetch a single article by its primary key ID

        :param article_id: int, the primary key of the article
        :return: dict or None, the article record or None if not found
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                        SELECT *
                        FROM feeds.articles
                        WHERE id = %s
                        """, (article_id,))
            article = cur.fetchone()
            return article

    def insert_article_classification(self, article_id: int, is_genai_related: bool, innovation_count: int):
        """
        Insert or update the GenAI classification for a given article.

        :param article_id: int, the primary key of the article
        :param is_genai_related: bool, whether the article is related to GenAI
        :param innovation_count: int, number of GenAI innovations found
        :return: None
        """
        self.logger.debug(
            "Inserting/updating article classification: article_id=%s, is_genai_related=%s, innovation_count=%d",
            article_id, is_genai_related, innovation_count
        )
        with self.conn.cursor() as cur:
            cur.execute("""
                        INSERT INTO feeds.article_classification (article_id, is_genai_related, innovation_count)
                        VALUES (%s, %s, %s) ON CONFLICT (article_id) DO
                        UPDATE
                            SET is_genai_related = EXCLUDED.is_genai_related,
                            innovation_count = EXCLUDED.innovation_count,
                            classified_at = now();
                        """, (article_id, is_genai_related, innovation_count))
        self.conn.commit()

    def get_genai_related_articles(self):
        """
        Retrieve all articles classified as GenAI related along with their classification details.

        :return: list of dicts, each containing article fields plus classification fields
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                        SELECT a.id
                        FROM feeds.articles a
                                 JOIN feeds.article_classification c ON a.id = c.article_id
                        WHERE c.is_genai_related = TRUE
                        ORDER BY a.published_at DESC NULLS LAST, a.created_at DESC;
                        """)
            rows = cur.fetchall()
            self.logger.debug("Fetched %d GenAI related articles", len(rows))
            return [row['id'] for row in rows]

def enqueue_article(config: dict, article_id: int, queue_name: str = 'default'):
    """
    Enqueue the PostgreSQL article ID into the Redis queue.

    :param config: Configuration dictionary
    :param article_id: The article's PostgreSQL ID to enqueue
    :param queue_name: The name of the RQ queue (default 'default')
    """
    redis_conn = Redis(**config)
    q = Queue(queue_name, connection=redis_conn)
    q.enqueue('tasks.classify_article', article_id)
