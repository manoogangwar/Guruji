// Object to manage profile completion data cache
const PROFILE_COMPLETION_CACHE_KEY = 'profileCompletionCache';
const CACHE_EXPIRY_DURATION = 600000; // 10 minutes in milliseconds
const COMPLETE_PROFILE_POPUP_KEY = 'completeProfilePopupKey'

// Function to fetch profile completion percentage from the server
async function fetchProfileCompletion() {
    try {
        const response = await fetch('/accounts/api/profile-completion/');
        if (!response.ok) {
            throw new Error(`Error fetching profile completion: ${response.statusText}`);
        }

        const data = await response.json();
        
        // Update local storage cache
        const cacheData = {
            percentage: data.profile_completion_percentage,
            lastUpdated: Date.now()
        };
        localStorage.setItem(PROFILE_COMPLETION_CACHE_KEY, JSON.stringify(cacheData));
        // Update UI
        updateProfileCompletionUI(data.profile_completion_percentage);
    } catch (error) {
        //console.error(error);
    }
}

function showProfileComplete(percentage){
    
    if(percentage < 85 ){
        if (document.getElementById('profileCompletionOffcanvas')) {
            const offcanvasElement = document.getElementById('profileCompletionOffcanvas');
            offcanvasElement.querySelector('.profile_percent').innerHTML = `${percentage}%`;
            if(offcanvasElement.querySelector('a').href != window.location.href){

                const offcanvas = new bootstrap.Offcanvas(offcanvasElement);
                offcanvas.show();
            }
            
          }
    }
}
// Function to update the UI with the profile completion percentage
function updateProfileCompletionUI(percentage) {
    const progressCircle = document.querySelector('.profile-circle-pregress');
    const percentageText = document.querySelector('.nav-tooltip');

    if (progressCircle) {
        const circumference = 282.6; // Assuming this is the SVG circle's circumference
        const offset = circumference - (percentage / 100) * circumference;
        progressCircle.style.strokeDashoffset = offset;
    }

    if (percentageText) {
        percentageText.setAttribute('data-bs-original-title', `Profile ${percentage}% completed`);
    }
    
    setTimeout(()=>{
        showProfileComplete(percentage)
    },40000)
    

}

// Function to manually update the profile completion percentage after a form submission
function updateProfileAfterFormSubmit() {
    // Fetch and update data after a form is submitted
    fetchProfileCompletion();
}

// Function to load data from cache if valid
function loadCachedProfileCompletion() {
    const cachedData = localStorage.getItem(PROFILE_COMPLETION_CACHE_KEY);

    if (cachedData) {
        const cache = JSON.parse(cachedData);

        // Check if the cache is still valid
        if (Date.now() - cache.lastUpdated < CACHE_EXPIRY_DURATION) {
            updateProfileCompletionUI(cache.percentage);
            return true;
        }
       
    }

    // Cache is invalid or doesn't exist
    return false;
}

// Initial fetch of profile completion percentage on page load
document.addEventListener('DOMContentLoaded', () => {
    if (!loadCachedProfileCompletion()) {
        // Fetch only if no valid cache exists
        fetchProfileCompletion();
    }
});
