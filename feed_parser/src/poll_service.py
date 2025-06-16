import feedparser

from common.mixins import LoggerMixin


class PollService(LoggerMixin):
    """Polls RSS feeds."""

    def poll(self, feed: dict):
        """Polls a single RSS feed.

        :param feed: Dictionary containing feed metadata (e.g., url, etag)
        """

        self.logger.info(f"Polling: {feed['url']} (id={feed['id']})")

        headers = {}
        if feed.get('etag'):
            headers['If-None-Match'] = feed['etag']
        if feed.get('last_modified'):
            headers['If-Modified-Since'] = feed['last_modified']

        parsed = feedparser.parse(feed['url'], request_headers=headers)
        if parsed.status == 304:
            self.logger.info('No new entries (304 Not Modified).')
            return None

        self.logger.info(f"Found {len(parsed.entries)} new entries.")
        for entry in parsed.entries:
            self.logger.debug(f"- {entry.title}")
        return parsed
