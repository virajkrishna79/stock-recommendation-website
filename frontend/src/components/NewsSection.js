import React, { useState, useEffect } from 'react';

const NewsSection = () => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchNews();
  }, []);

  const fetchNews = async () => {
    try {
      setLoading(true);
      setError('');
      const backendUrl = process.env.REACT_APP_BACKEND_URL;
      const response = await fetch(`${backendUrl}/api/news`);
      const data = await response.json();
      
      if (data.success) {
        setNews(data.news);
      } else {
        setError('Failed to fetch news');
      }
    } catch (err) {
      setError('Error connecting to news service');
      console.error('Error fetching news:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    try {
      return new Date(dateString).toLocaleDateString('en-IN', {
        day: 'numeric',
        month: 'short',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return dateString;
    }
  };

  if (loading) {
    return (
      <div className="news-section max-w-6xl mx-auto px-4 py-8">
        <h2 className="text-2xl font-bold mb-6">📰 Latest Financial News</h2>
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading latest news...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="news-section max-w-6xl mx-auto px-4 py-8">
        <h2 className="text-2xl font-bold mb-6">📰 Latest Financial News</h2>
        <div className="text-center py-8 text-red-500">
          <p>{error}</p>
          <button 
            onClick={fetchNews}
            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="news-section max-w-6xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">📰 Latest Financial News</h2>
        <button 
          onClick={fetchNews}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
        >
          Refresh
        </button>
      </div>

      {news.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          <p>No news available at the moment.</p>
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {news.map((item, index) => (
            <div 
              key={index} 
              className="bg-white rounded-lg shadow-md border border-gray-200 hover:shadow-lg transition-shadow p-6"
            >
              <div className="flex justify-between items-start mb-3">
                <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded">
                  {item.source}
                </span>
                {item.published && (
                  <span className="text-xs text-gray-500">
                    {formatDate(item.published)}
                  </span>
                )}
              </div>
              
              <h3 className="font-semibold text-lg mb-3 line-clamp-3">
                <a 
                  href={item.link} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-gray-900 hover:text-blue-600 transition-colors"
                >
                  {item.title}
                </a>
              </h3>
              
              {item.summary && (
                <p className="text-gray-600 text-sm line-clamp-3 mb-4">
                  {item.summary}
                </p>
              )}
              
              <a 
                href={item.link} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-blue-500 hover:text-blue-700 text-sm font-medium"
              >
                Read more →
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default NewsSection;