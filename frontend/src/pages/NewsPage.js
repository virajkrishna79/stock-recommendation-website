import React, { useEffect, useState } from 'react';
import NewsCard from '../components/NewsCard';
import { fetchNews } from '../services/api';

const NewsPage = () => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        setError('');
        const items = await fetchNews(18);
        setNews(items);
      } catch (e) {
        setError('Failed to load news');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Latest Financial News</h1>
        <button
          onClick={async () => {
            try {
              setLoading(true);
              const items = await fetchNews(18);
              setNews(items);
            } finally {
              setLoading(false);
            }
          }}
          className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
        >
          Refresh
        </button>
      </div>

      {loading ? (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(6)].map((_, idx) => (
            <div key={idx} className="news-card animate-pulse">
              <div className="skeleton-title mb-3" />
              <div className="skeleton-text mb-2" />
              <div className="skeleton-text mb-2" />
              <div className="skeleton-text mb-4" />
            </div>
          ))}
        </div>
      ) : error ? (
        <div className="text-red-600">{error}</div>
      ) : news.length === 0 ? (
        <div className="text-gray-600">No news available right now.</div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {news.map((article, idx) => (
            <NewsCard key={idx} article={article} />
          ))}
        </div>
      )}
    </div>
  );
};

export default NewsPage;
