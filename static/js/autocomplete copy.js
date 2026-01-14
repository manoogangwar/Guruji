// autocomplete.js
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('user-search');
    const suggestions = document.getElementById('suggestions');
    let debounceTimeout;

    searchInput.addEventListener('keyup', function () {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(() => {
            const query = searchInput.value.replace(/^\s+|\s+$/g, "");
            console.log('request sent')
            if (query.length > 1) {  // Start searching after 2 characters
                const query = searchInput.value.replace(/^\s+|\s+$/g, "");
                fetch(`/user-search/?q=${query}`)
                    .then(response => response.json())
                    .then(data => {
                        suggestions.innerHTML = '';  // Clear previous suggestions
                        suggestions.style.display = 'block'
                        if (data.length > 0) {
                            data.forEach(user => {
                                const suggestionItem = document.createElement('div');
                                suggestionItem.innerHTML = '<i class="bi bi-search fs-6"></i>'+' ' + user.name;
                                suggestionItem.setAttribute('data-id', user.id);
                                suggestionItem.classList.add('suggestion-item');
                                suggestions.appendChild(suggestionItem);
                            });
                        } else {
                            const noResultItem = document.createElement('div');
                            noResultItem.textContent = `no result for '${query}'`;
                            noResultItem.classList.add('no-result-item');
                            suggestions.appendChild(noResultItem);
                        }
                    });
            } else {
                suggestions.style.display = 'none'
                suggestions.innerHTML = '';  // Clear suggestions if query is too short
            }
        }, 500);  // Debounce timeout of 500 milliseconds
    });

    // Optional: Handle suggestion item click
    suggestions.addEventListener('click', function (event) {
        if (event.target.classList.contains('suggestion-item')) {
            const userId = event.target.getAttribute('data-id');
            searchInput.value = event.target.textContent.replace(/^\s+|\s+$/g, "");
            suggestions.innerHTML = '';  // Clear suggestions
            // Optionally, redirect or take another action
            console.log(`Selected user ID: ${userId}`);
        }
    });
});
