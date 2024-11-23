from flask import Blueprint, render_template, url_for
import os
import json

news_bp = Blueprint('news', __name__)

ARTICLES_FOLDER = 'articles'

def load_articles():
    articles = []
    for filename in os.listdir(ARTICLES_FOLDER):
        filepath = os.path.join(ARTICLES_FOLDER, filename)
        if filename.endswith('.json') or filename.endswith('.txt'):
            with open(filepath, 'r') as file:
                try:
                    if filename.endswith('.json'):
                        article = json.load(file)
                    else:
                        content = file.read()
                        lines = content.splitlines()
                        article = {
                            "id": int(lines[0].strip()),
                            "title": lines[1].strip(),
                            "preview": lines[2].strip(),
                            "content": "\n".join(lines[3:]),
                            "image": "../static/img/default.jpg"
                        }
                    articles.append(article)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
    return articles

@news_bp.route('/news')
def news_page():
    articles = load_articles()
    return render_template('news.html', articles=articles)

@news_bp.route('/article/<int:article_id>')
def article_page(article_id):
    articles = load_articles()
    article = next((a for a in articles if a['id'] == article_id), None)
    if not article:
        return render_template('404.html'), 404
    return render_template('article.html', article=article)
