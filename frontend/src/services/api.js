export const fetchNews = async (limit = 10) => {
  console.log('fetchNews called with limit:', limit);
  
  try {
    const backendUrl = 'https://stock-recommendation-website-production.up.railway.app';
    console.log('Fetching from:', `${backendUrl}/api/news?limit=${limit}`);
    
    const response = await fetch(`${backendUrl}/api/news?limit=${limit}`);
    console.log('Response status:', response.status);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log('Response data:', data);
    
    if (data.success) {
      console.log('News count:', data.news.length);
      // Normalize fields for UI components like NewsCard
      const normalized = (data.news || []).map((n) => ({
        title: n.title || n.headline || '',
        description: n.description || n.summary || '',
        url: n.url || n.link || '#',
        source: n.source || 'Financial News',
        published_at: n.published_at || n.published || new Date().toISOString(),
        sentiment_score: n.sentiment_score ?? null,
        sentiment_label: n.sentiment_label || 'neutral',
      }));
      return normalized;
    } else {
      throw new Error(data.error || 'Failed to fetch news');
    }
  } catch (error) {
    console.error('Error in fetchNews:', error);
    throw error;
  }
};

export const subscribeToNewsletter = async (email) => {
  console.log('subscribeToNewsletter called with email:', email);
  
  try {
    const backendUrl = 'https://stock-recommendation-website-production.up.railway.app';
    console.log('Subscribing to:', `${backendUrl}/api/newsletter/subscribe`);
    
    const response = await fetch(`${backendUrl}/api/newsletter/subscribe`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email }),
    });
    
    console.log('Subscription response status:', response.status);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log('Subscription response data:', data);
    
    if (data.success) {
      console.log('Subscription successful');
      return data;
    } else {
      throw new Error(data.error || 'Failed to subscribe to newsletter');
    }
  } catch (error) {
    console.error('Error in subscribeToNewsletter:', error);
    throw error;
  }
};
