// autocomplete with cache

document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('location-search');
    const suggestions = document.getElementById('location-suggestions');
    let debounceTimeout;
    const cache = {};  // Initialize cache object
    
    searchInput.addEventListener('keyup', function () {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(() => {
            const query = searchInput.value.replace(/^\s+|\s+$/g, "");
            if (query.length > 1) {  // Start searching after 2 characters
                if (cache[query]) {
                    displaySuggestions(cache[query], query);
                } else {
                    fetch(`https://nominatim.openstreetmap.org/search?q=${query}&limit=5&format=json&addressdetails=1`)
                        .then(response => response.json())
                        .then(data => {
                            cache[query] = data;  // Store results in cache
                            displaySuggestions(data, query);
                        });
                }
            } else {
                suggestions.style.display = 'none';
                suggestions.innerHTML = '';  // Clear suggestions if query is too short
            }
        }, 500);  // Debounce timeout of 500 milliseconds
    });

    // Optional: Handle suggestion item click
    suggestions.addEventListener('click', function (event) {
        suggestions.style.display = 'none';
        if (event.target.classList.contains('suggestion-item')) {
            const userId = event.target.getAttribute('data-id');
            searchInput.value = event.target.textContent.replace(/^\s+|\s+$/g, "");
            suggestions.innerHTML = '';  // Clear suggestions           
        }
    });

  

    function displaySuggestions(data, query) {
        suggestions.innerHTML = '';  // Clear previous suggestions
        suggestions.style.display = 'block';
        if (data.length > 0) {
            data.forEach(user => {    
                sgItem = `<li class='suggestion-item text-truncate cursor-pointer' data-id='${user.osm_id}'>${user.display_name} <span class="text-muted"> </span> </li>`;
                suggestions.innerHTML += sgItem;
            });
        } else {
            const noResultItem = document.createElement('li');
            noResultItem.textContent = `no result for '${query}'`;
            noResultItem.classList.add('no-result-item');
            suggestions.appendChild(noResultItem);
        }
    }


});
