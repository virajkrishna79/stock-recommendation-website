from flask import Blueprint, request, jsonify, render_template
from models import User, StockRecommendation, NewsArticle
from services.stock_service import StockService
from services.news_service import NewsService
from services.recommendation_service import RecommendationService
from services.email_service import EmailService
from app import db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprints
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)

# Initialize services
stock_service = StockService()
news_service = NewsService()
recommendation_service = RecommendationService()
email_service = EmailService()

@main_bp.route('/')
def index():
    """Main homepage with news and subscription form"""
    try:
        # Get latest news
        news = news_service.get_latest_news(limit=10)
        return render_template('index.html', news=news)
    except Exception as e:
        logger.error(f"Error loading homepage: {e}")
        return render_template('index.html', news=[])

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@api_bp.route('/subscribe', methods=['POST'])
def subscribe():
    """Subscribe user to stock recommendations"""
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            if existing_user.is_active:
                return jsonify({'message': 'Email already subscribed'}), 200
            else:
                existing_user.is_active = True
                db.session.commit()
                return jsonify({'message': 'Subscription reactivated successfully'}), 200
        
        # Create new user
        new_user = User(email=email)
        db.session.add(new_user)
        db.session.commit()
        
        # Send confirmation email
        try:
            email_service.send_confirmation_email(email)
        except Exception as e:
            logger.warning(f"Failed to send confirmation email: {e}")
        
        return jsonify({'message': 'Subscription successful!'}), 201
        
    except Exception as e:
        logger.error(f"Error in subscription: {e}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    """Unsubscribe user from stock recommendations"""
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        user = User.query.filter_by(email=email).first()
        if user:
            user.is_active = False
            db.session.commit()
            return jsonify({'message': 'Unsubscribed successfully'}), 200
        else:
            return jsonify({'error': 'Email not found'}), 404
            
    except Exception as e:
        logger.error(f"Error in unsubscription: {e}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

# ==== KEEP THIS ENHANCED NEWS ROUTE ====
@api_bp.route('/news', methods=['GET'])
def get_news():
    """Get latest financial news - API endpoint"""
    try:
        category = request.args.get('category', 'latest')
        limit = int(request.args.get('limit', 15))
        
        news = news_service.get_news(category=category, limit=limit)
        
        return jsonify({
            'success': True,
            'news': news,
            'count': len(news)
        })
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch news'
        }), 500

@api_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    """Get stock recommendations"""
    try:
        symbol = request.args.get('symbol')
        if symbol:
            recommendations = recommendation_service.get_recommendations_for_symbol(symbol)
        else:
            recommendations = recommendation_service.get_latest_recommendations()
        
        return jsonify({'recommendations': recommendations})
    except Exception as e:
        logger.error(f"Error fetching recommendations: {e}")
        return jsonify({'error': 'Failed to fetch recommendations'}), 500

@api_bp.route('/stock/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    """Get stock data and recommendation for a specific symbol"""
    try:
        stock_data = stock_service.get_stock_data(symbol)
        recommendation = recommendation_service.get_recommendation_for_symbol(symbol)
        
        return jsonify({
            'symbol': symbol,
            'stock_data': stock_data,
            'recommendation': recommendation
        })
    except Exception as e:
        logger.error(f"Error fetching stock data for {symbol}: {e}")
        return jsonify({'error': f'Failed to fetch data for {symbol}'}), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'stock-recommendation-api'})

@api_bp.route('/news/markets', methods=['GET'])
def get_market_news():
    """Get stock market specific news - API endpoint"""
    try:
        news = news_service.get_market_news()
        
        return jsonify({
            'success': True,
            'news': news
        })
    except Exception as e:
        logger.error(f"Error fetching market news: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch market news'
        }), 500

@api_bp.route('/news/categories', methods=['GET'])
def get_news_categories():
    """Get available news categories"""
    return jsonify({
        'success': True,
        'categories': [
            'latest', 'markets', 'business', 'tech'
        ]
    })
