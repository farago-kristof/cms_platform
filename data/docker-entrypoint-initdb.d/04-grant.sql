-- User created in 01-create-user.sh
GRANT USAGE ON SCHEMA feeds TO cms_user;

GRANT INSERT, UPDATE, DELETE, SELECT ON feeds.rss_feed TO cms_user;

GRANT INSERT, SELECT ON feeds.articles TO cms_user;
GRANT USAGE, SELECT ON SEQUENCE feeds.articles_id_seq TO cms_user;
GRANT UPDATE ON SEQUENCE feeds.articles_id_seq TO cms_user;

GRANT INSERT, UPDATE, SELECT ON feeds.article_classification TO cms_user;
GRANT UPDATE ON SEQUENCE feeds.article_classification_id_seq TO cms_user;