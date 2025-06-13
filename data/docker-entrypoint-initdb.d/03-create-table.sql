CREATE TABLE IF NOT EXISTS feeds.rss_feed (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL UNIQUE,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    last_polled TIMESTAMPTZ,
    last_updated TIMESTAMPTZ,
    etag TEXT,
    last_modified TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE OR REPLACE FUNCTION feeds.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_updated_at
BEFORE UPDATE ON feeds.rss_feed
FOR EACH ROW
EXECUTE FUNCTION feeds.update_updated_at_column();

CREATE TABLE IF NOT EXISTS feeds.articles (
    id SERIAL PRIMARY KEY,
    feed_id INTEGER NOT NULL REFERENCES feeds.rss_feed(id) ON DELETE CASCADE,
    title VARCHAR(256) NOT NULL,
    link VARCHAR(512) NOT NULL UNIQUE,
    published_at TIMESTAMP WITH TIME ZONE,
    content TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
