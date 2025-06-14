from flask import Flask, jsonify

from common.db import CMSDataBase
from config import POSTGRES_CONNECTION

app = Flask(__name__)

@app.route('/api/gen_ai_articles')
def get_gen_ai_articles():
    with CMSDataBase(POSTGRES_CONNECTION) as db:
        articles = db.get_all_articles()
    return jsonify({'article_ids': articles})

@app.route('/api/articles/<int:article_id>')
def get_article(article_id):
    with CMSDataBase(POSTGRES_CONNECTION) as db:
        article = db.get_article_by_id(article_id)
        if not article:
            return jsonify({'error': 'Article not found'}), 404
    return jsonify(article)
