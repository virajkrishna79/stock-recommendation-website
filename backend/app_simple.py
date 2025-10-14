from flask import Flask, jsonify
from flask_cors import CORS
import feedparser

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "Stock Recommendation API"})

@app.route('/api/news')
def get_news():
    """Simple news endpoint without database"""
    try:
        feed = feedparser.parse("https://www.moneycontrol.com/rss/latestnews.xml")
        news_items = []
        
        for entry in feed.entries[:10]:
            news_items.append({
                'title': entry.title,
                'link': entry.link,
                'summary': entry.get('summary', ''),
                'published': entry.get('published', ''),
                'source': 'MoneyControl'
            })
        
        return jsonify({
            'success': True,
            'news': news_items
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)