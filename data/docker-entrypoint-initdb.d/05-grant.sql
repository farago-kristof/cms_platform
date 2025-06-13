-- User created in 01-create-user.sh
GRANT USAGE ON SCHEMA feeds TO cms_user;
GRANT INSERT, SELECT ON feeds.rss_feed TO cms_user;