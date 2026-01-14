document.addEventListener('DOMContentLoaded', () => {
    const megamenuLink = document.querySelector('.megamenu-link');
    const eventsList = document.getElementById('megamenu-events-list');
    
    const storageKey = 'cachedEvents';

    // Function to fetch events (simulated API fetch)
    const fetchEvents = async () => {
        try {
            const response = await fetch('/events/api/events/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
    
            if (!response.ok) {
                throw new Error('Failed to fetch events');
            }
    
            const data = await response.json();
            return data; // Assumes the API returns an array of events
        } catch (error) {
            console.error('Error fetching events:', error);
            return [];
        }
    };
    

    // Function to cache events in localStorage
    const cacheEvents = (events) => {
        localStorage.setItem(storageKey, JSON.stringify(events));
    };

    // Function to retrieve cached events from localStorage
    const getCachedEvents = () => {
        const cached = localStorage.getItem(storageKey);
        return cached ? JSON.parse(cached) : [];
    };

    // Function to render events in the mega menu
    const renderEvents = (events) => {
        eventsList.innerHTML = '';
        if (events.length > 0) {
            events.forEach((event) => {
                const listItem = document.createElement('li');
                listItem.textContent = `${event.title} - ${event.date}`;
                eventsList.appendChild(listItem);
            });
        } else {
            eventsList.innerHTML = '<li>No events available.</li>';
        }
    };

    // Function to update events dynamically
    const updateEvents = async () => {
        const events = await fetchEvents();
        cacheEvents(events); // Cache the fetched events
        renderEvents(events); // Update the UI
    };

    // Check for cached events and render them
    const cachedEvents = getCachedEvents();
    if (cachedEvents.length > 0) {
        renderEvents(cachedEvents);
    } else {
        updateEvents(); // Fetch and update if no cache
    }

    // Optional: Refresh events when the mega menu link is clicked
    megamenuLink.addEventListener('click', async () => {
        await updateEvents(); // Fetch and update events on-demand
    });
});
