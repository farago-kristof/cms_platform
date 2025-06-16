from flask import Flask, jsonify
from flask_cors import CORS

from common.db import CMSDataBase
from config import POSTGRES_CONNECTION

app = Flask(__name__)

CORS(app, resources={r"/articles/*": {"origins": "https://articles.localhost"}})

@app.route('/articles/gen_ai')
def get_gen_ai_articles():
    with CMSDataBase(POSTGRES_CONNECTION) as db:
        articles = db.get_genai_related_articles()
    return jsonify({'article_ids': articles})

@app.route('/articles/<int:article_id>')
def get_article(article_id):
    with CMSDataBase(POSTGRES_CONNECTION) as db:
        article = db.get_article_by_id(article_id)
        if not article:
            return jsonify({'error': 'Article not found'}), 404
    return jsonify(article)
