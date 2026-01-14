// autocomplete with cache

document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('user-search');
    const suggestions = document.getElementById('suggestions');
    let location = document.getElementById('location-search').value
    let debounceTimeout;
    const cache = {};  // Initialize cache object
    
    searchInput.addEventListener('keyup', function () {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(() => {
            const query = searchInput.value.replace(/^\s+|\s+$/g, "");
            
            if (query.length > 1) {  // Start searching after 2 characters
                if (cache[query]) {
                    // Use cached results
                    displaySuggestions(cache[query], query);
                    // console.log('cache called sent')
                } else {
                    // console.log('request sent')
                    fetch(`/user-search/?q=${query}&l=${location}`)
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
            const userName = event.target.getAttribute('data-name')
            //searchInput.value = event.target.textContent.replace(/^\s+|\s+$/g, "");
            searchInput.value = userName;
            suggestions.innerHTML = '';  // Clear suggestions
            // Optionally, redirect or take another action
            // console.log(`Selected user ID: ${userId}`);
            //window.open(`/@${userId}`,'_self')
        }else{
            searchInput.value = event.target.getAttribute('data');
        }
        // searchInput.value = event.target.textContent.replace(/^\s+|\s+$/g, "");
        // console.log(event.target)

    });

  

    function displaySuggestions(data, query) {
        suggestions.innerHTML = '';  // Clear previous suggestions
        suggestions.style.display = 'block';
        if (data.length > 0) {
            data.forEach(user => {
                // const suggestionItem = document.createElement('li');
                // suggestionItem.innerHTML = '<i class="bi bi-search fs-6"></i>' + ' ' + user.name;
                // suggestionItem.setAttribute('data-id', user.id);
                // suggestionItem.classList.add('suggestion-item');
                // suggestions.appendChild(suggestionItem);
                
                if(user.profession != null)    
                    {sgItem = `<li class='suggestion-item text-truncate cursor-pointer' data-id='${user.id}' data-name='${user.name}' ><i class="bi bi-search fs-6"></i> ${user.name} <span class="text-muted"> | ${user.profession} </span> </li>`}
                else{
                    sgItem = `<li class='suggestion-item text-truncate cursor-pointer' data-id='${user.id}' data-name='${user.name}' ><i class="bi bi-search fs-6"></i> ${user.name} <span class="text-muted"></span> </li>`}

                suggestions.innerHTML += sgItem


                
            });
        } else {
            const noResultItem = document.createElement('li');
            noResultItem.textContent = `no result for '${query}'`;
            noResultItem.classList.add('no-result-item');
            suggestions.appendChild(noResultItem);
        }
    }

    // handle focous out 
    searchInput.addEventListener("focusout",(e)=>{
        // suggestions.style.display = 'none'
    });


});
