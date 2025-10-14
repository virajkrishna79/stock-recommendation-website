// frontend/src/services/api.js

export const fetchNews = async (limit = 10) => {
  try {
    // Use your actual Railway backend URL directly
    const backendUrl = 'https://stock-recommendation-website-production.up.railway.app';
    const response = await fetch(`${backendUrl}/api/news?limit=${limit}`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch news');
    }
    
    const data = await response.json();
    
    if (data.success) {
      return data.news;
    } else {
      throw new Error(data.error || 'Failed to fetch news');
    }
  } catch (error) {
    console.error('Error fetching news:', error);
    throw error;
  }
};

// You can add other API functions here later as needed
