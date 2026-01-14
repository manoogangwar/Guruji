document.addEventListener('DOMContentLoaded', () => {
    const megamenuLink = document.querySelector('.megamenu-link');
    const newsList = document.getElementById('megamenu-news-list');
    const storageKey = 'cachedNews';

    // Function to fetch news (simulated API fetch)
    const fetchNews = async () => {
        try {
            const response = await fetch('/news/api/news/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            
            if (!response.ok) {
                throw new Error('Failed to fetch news');
            }
    
            const data = await response.json();
            return data; // Assumes the API returns an array of news
        } catch (error) {
            console.error('Error fetching news:', error);
            return [];
        }
    };
    

    // Function to cache news in localStorage
    const cacheNews = (news) => {
        localStorage.setItem(storageKey, JSON.stringify(news));
    };

    // Function to retrieve cached news from localStorage
    const getCachedNews = () => {
        const cached = localStorage.getItem(storageKey);
        return cached ? JSON.parse(cached) : [];
    };

    // Function to render news in the mega menu
    const renderNews = (news) => {
        newsList.innerHTML = '';
        if (news.length > 0) {
            news.forEach((event) => {
                const listItem = document.createElement('li');
                listItem.textContent = `${event.title} - ${event.date}`;
                newsList.appendChild(listItem);
            });
        } else {
            newsList.innerHTML = '<li>No news available.</li>';
        }
    };

    // Function to update news dynamically
    const updateNews = async () => {
        const news = await fetchNews();
        cacheNews(news); // Cache the fetched news
        renderNews(news); // Update the UI
    };

    // Check for cached news and render them
    const cachedNews = getCachedNews();
    if (cachedNews.length > 0) {
        renderNews(cachedNews);
    } else {
        updateNews(); // Fetch and update if no cache
    }

    // Optional: Refresh news when the mega menu link is clicked
    megamenuLink.addEventListener('click', async () => {
        await updateNews(); // Fetch and update news on-demand
    });
});
