

document.getElementById('peronal_details_form').addEventListener('submit',function(event){
    event.preventDefault(); // Prevent submission if any validation fails
    const form = event.target; // Get the form element
    const formErrorContainer = form.querySelector('.error-message');

    const formIsValid =validatePostalCode() && validateCity() && validateState() && validateCountry() && validateAddress() &&  validateNameTitle() && validateFirstName() && validateLastName() && validateDOB() && validateGender() && requiredCheck() && validateLinkedIn() && validateFacebook() && validateInstagram() && validateTwitter();
    if (formIsValid) {
        submitForm(event,'peronal_details_form',`/accounts/profile_handler`);
    }
    else if (formErrorContainer) {
        formErrorContainer.style.color = 'red';
        formErrorContainer.textContent = 'There is an error in the form. Please review and correct the errors.';
    }
    return false
})

document.getElementById('password_change').addEventListener('submit',function(event){
    event.preventDefault(); // Prevent form submission if validation fails

    const isOldPasswordValid = validateOldPassword();
    const isNewPassword1Valid = validateNewPassword1();
    const isNewPassword2Valid = validateNewPassword2();
    if (isOldPasswordValid && isNewPassword1Valid && isNewPassword2Valid) {
        submitForm(event,'password_change',`/accounts/password_change_handler`)
    }
})

document.getElementById('username_change').addEventListener('submit',function(event){
    event.preventDefault()
    if(validateUsername()){
        submitForm(event,'username_change',`/accounts/username_change_handler`)
    }
})

document.getElementById('email_change').addEventListener('submit',function(event){
    submitForm(event,'email_change',`/accounts/email_change_handler`)
})

document.getElementById('communication_preferences').addEventListener('submit',function(event){
    submitForm(event,'communication_preferences',`/accounts/communication_handler`)
})

document.getElementById('volunteer_form').addEventListener('submit',function(event){
    submitForm(event,'volunteer_form',`/accounts/volunteer_handler`)
})
document.getElementById('member_profile_form').addEventListener('submit',function(event){
    event.preventDefault(); // Prevent form submission if validation fails

    const isBioValid = validateBio();
    const isProfilePictureValid = validateProfilePicture();
    const isBloodGroupValid = validateBloodGroup();
    if (isBioValid && isProfilePictureValid && isBloodGroupValid) {
        submitForm(event,'member_profile_form',`/accounts/member_profile_handler`)
        
        const file = document.getElementById('id_profile_picture').files[0]; // Get the selected file
        if (file) {
            const reader = new FileReader();

            // When the file is loaded
            reader.onload = (e) => {
                const newImageSrc = e.target.result; // Get the base64 encoded image source

                // Find all images with the class 'profile-image' and update their source
                const profileImages = document.querySelectorAll('.profile-image');
                profileImages.forEach((image) => {
                    image.src = newImageSrc;
                });
            };

            // Read the selected image file
            reader.readAsDataURL(file);
        }


    }
    
})

document.getElementById('professional_form').addEventListener('submit',function(event){
    submitForm(event,'professional_form',`/accounts/professional_handler`)
})
// document.getElementById('username_change').addEventListener('submit',function(event){
//     submitForm(event,'username_change',`{% url 'change_username' %}`)
// })

document.getElementById('privacy_form').addEventListener('submit',function(event){
    submitForm(event,'privacy_form',`/accounts/privacy_handler`)
})


function showError(element, message) {
        element.classList.add("is-invalid");
        let errorNode = document.createElement("small");
        errorNode.classList.add("text-danger");
        errorNode.innerText = message;
        element.parentNode.appendChild(errorNode);
    }

function clearError(element) {
    element.classList.remove("is-invalid");
    let errorNode = element.parentNode.querySelector(".text-danger");
    if (errorNode) {
        errorNode.remove();
    }
}    

async function submitForm(event, formId, url) {
    event.preventDefault(); // Prevent the default form submission
    const form = document.getElementById(formId);

    const formData = new FormData(form); // Collect form data
    const errorDiv = form.querySelector('.error-message');
    errorDiv.textContent = ''; // Clear previous error messages

    // Remove previous error indicators and messages
    form.querySelectorAll(".is-invalid").forEach((el) => {
        el.classList.remove("is-invalid");
        const errorMsg = el.parentNode.querySelector("small.text-danger");
        if (errorMsg) {
            errorMsg.remove();
        }
    });

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: formData,
        });

        if (response.ok) {
            const result = await response.json();
            if (result.success) {
                errorDiv.textContent = 'Changes Updated successfully!';
                errorDiv.style.color = 'green';
            } else {
                // Show validation errors from Django
                const errors = JSON.parse(result.error);
                for (let field in errors) {
                    const fieldElement = form.querySelector(`[name="${field}"]`);
                    if (fieldElement) {
                        showError(fieldElement, errors[field][0].message);
                    }
                }
            }
        } else {
            // If there's a server error (not validation errors)
            const error = await response.json();
            errorDiv.textContent = error.error || 'Submission failed. Please try again.';
            errorDiv.style.color = 'red';
        }
    } catch (error) {
        console.error('Fetch error:', error);
        errorDiv.textContent = 'An error occurred. Please try again.';
        errorDiv.style.color = 'red';
    }
}

// form validation codes
function validatePhonePrefix() {
        const phonePrefixInput = document.getElementById("id_phone_prefix");
        const phonePrefix = phonePrefixInput.value.trim();
        clearError(phonePrefixInput);

        if (phonePrefix === "") {
            showError(phonePrefixInput, "Phone prefix is required.");
            return false;
        }
        return true;
    }

    function validatePhoneNumber() {
        const phoneNumberInput = document.getElementById("id_phone_number");
        const phoneNumber = phoneNumberInput.value.trim();
        clearError(phoneNumberInput);

        if (phoneNumber === "") {
            showError(phoneNumberInput, "Phone number is required.");
            return false;
        }

        const phoneRegex = /^[0-9]{10}$/;
        if (!phoneRegex.test(phoneNumber)) {
            showError(phoneNumberInput, "Phone number must be 10 digits.");
            return false;
        }
        return true;
    }


    function validateEmail() {
        const emailInput = document.getElementById("id_email");
        const email = emailInput.value.trim();
        clearError(emailInput);

        if (email === "") {
            showError(emailInput, "Email is required.");
            return false;
        }

        const emailRegex = /^[\w.%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/i;
        if (!emailRegex.test(email)) {
            showError(emailInput, "Invalid email format.");
            return false;
        }
        return true;
    }

    function isUrlOrContainsSlash(str) {
        try {
            // Check if it's a valid URL
            new URL(str);
            return true;
        } catch (error) {
            // Check if it contains '/'
            return str.includes('/');
        }
    }

    function validateInstagram(){
        const instaInput = document.getElementById('id_instagram_link');
        if(instaInput){
            const link_icon = instaInput.parentElement.querySelector('a');
            link_icon.href = 'https://instagram.com/'+ instaInput.value

            const insta = instaInput.value.trim()
            clearError(instaInput.parentNode);
            if(!isUrlOrContainsSlash(insta)){
                return true
            }
            if(insta == ''){
                return true
            }
            showError(instaInput.parentNode, "Invalid instagram username. URLs are not allowed.");
            link_icon.href = '#';
            return false
        }
    }

    function validateTwitter() {
        const twitterInput = document.getElementById('id_twitter_link');
        if (twitterInput) {
            const twitterHandle = twitterInput.value.trim();
            clearError(twitterInput.parentNode);
            const link_icon = twitterInput.parentElement.querySelector('a');
            link_icon.href = 'https://x.com/'+twitterHandle;
    
            // Allow empty input
            if (twitterHandle === '') {
                return true;
            }

            // Ensure handle does not contain '/' or resemble a URL
            if (twitterHandle.includes('/') || twitterHandle.includes('http://') || twitterHandle.includes('https://')) {
                showError(twitterInput.parentNode, "Invalid Twitter (or X) handle. URLs are not allowed.");
                link_icon.href = '#'
                return false;
            }
    
            // Check if handle starts with '@'
            if (twitterHandle[0] !== '@') {
                showError(twitterInput.parentNode, "Invalid Twitter (or X) handle. It must start with '@'.");
                link_icon.href = '#'
                return false;
            }
    
            // Check minimum length (e.g., @a is invalid)
            if (twitterHandle.length < 2) {
                showError(twitterInput.parentNode, "Invalid Twitter (or X) handle. Too short.");
                link_icon.href = '#'
                return false;
            }

            return true; // Handle is valid
        }
    }

    function validateFacebook() {
        const facebookInput = document.getElementById('id_facebook_link');
        if (facebookInput) {
            const facebookLink = facebookInput.value.trim();
            clearError(facebookInput.parentNode);
            const link_icon = facebookInput.parentElement.querySelector('a');
            link_icon.href = facebookInput.value
            // Allow empty input
            if (facebookLink === '') {
                return true;
            }
    
            // Validate URL
            if (isValidUrl(facebookLink) && facebookLink.includes('facebook')) {
                return true;
            }
    
            showError(facebookInput.parentNode, "Invalid Facebook URL. Please provide a valid link.");
            link_icon.href = '#';
            return false;
        }
    }
    
    function validateLinkedIn() {
        const linkedInInput = document.getElementById('id_linkedin_link');
        if (linkedInInput) {
            const linkedInLink = linkedInInput.value.trim();
            clearError(linkedInInput.parentNode);
            const link_icon = linkedInInput.parentElement.querySelector('a');
            link_icon.href = linkedInInput.value
            // Allow empty input
            if (linkedInLink === '') {
                return true;
            }
            
            // Validate URL
            if (isValidUrl(linkedInLink) && linkedInLink.includes('linkedin')) {
                return true;
            }

    
            showError(linkedInInput.parentNode, "Invalid LinkedIn URL. Please provide a valid link.");
            link_icon.href = '#'
            return false;
        }
    }
    
    // Utility function to check if a string is a valid URL
    function isValidUrl(string) {
        try {
            new URL(string); // Will throw an error if invalid
            return true;
        } catch {
            return false;
        }
    }
    
    



    function validateAddress() {
        const addressInput = document.getElementById("id_address");
        const address = addressInput.value.trim();
        clearError(addressInput);

        if (address === "") {
            showError(addressInput, "Address is required.");
            return false;
        }
        return true;
    }

    function validateCountry() {
        const countryInput = document.getElementById("id_country");
        const country = countryInput.value.trim();
        clearError(countryInput);

        if (country === "") {
            showError(countryInput, "Country is required.");
            return false;
        }
        return true;
    }

    function validateState() {
        const stateInput = document.getElementById("id_state");
        const state = stateInput.value.trim();
        clearError(stateInput);

        if (state === "") {
            showError(stateInput, "State is required.");
            return false;
        }
        return true;
    }

    function validateCity() {
        const cityInput = document.getElementById("id_city");
        const city = cityInput.value.trim();
        clearError(cityInput);

        if (city === "") {
            showError(cityInput, "City is required.");
            return false;
        }
        return true;
    }

    function validatePostalCode() {
        const postalCodeInput = document.getElementById("id_postal_code");
        const postalCode = postalCodeInput.value.trim();
        clearError(postalCodeInput);

        if (postalCode === "") {
            showError(postalCodeInput, "Postal code is required.");
            return false;
        }

        const postalCodeRegex = /^[0-9]{5,6}$/;
        if (!postalCodeRegex.test(postalCode)) {
            showError(postalCodeInput, "Postal code must be 5 or 6 digits.");
            return false;
        }
        return true;
    }
    
    function validateOccupation() {
        const OccupationInput = document.getElementById("id_occupation_detail");
        clearError(OccupationInput);
        if (OccupationInput.value.trim() === "") {
            showError(OccupationInput, "Occupation is required.");
            return false;
        }
        return true;
    }
    
    function validateNameTitle() {
        const nameTitleInput = document.getElementById("id_name_title");
        clearError(nameTitleInput);
        if (nameTitleInput.value.trim() === "") {
            showError(nameTitleInput, "Please select a title.");
            return false;
        }
        return true;
    }
    function validateFirstName() {
        const firstNameInput = document.getElementById("id_first_name");
        clearError(firstNameInput);
        if (firstNameInput.value.trim() === "") {
            showError(firstNameInput, "First name is required.");
            return false;
        }
        return true;
    }
    function validateLastName() {
        const lastNameInput = document.getElementById("id_last_name");
        clearError(lastNameInput);
        // if (lastNameInput.value.trim() === "") {
        //     showError(lastNameInput, "Last name is required.");
        //     return false;
        // }
        return true;
    }
    function validateDOB() {
        const dobInput = document.getElementById("id_dob");
        clearError(dobInput);
        if (dobInput.value === "") {
            showError(dobInput, "Date of birth is required.");
            return false;
        }
        return true;
    }
    function validateGender() {
        const genderInput = document.getElementById("id_gender");
        clearError(genderInput);
        if (genderInput.value.trim() === "") {
            showError(genderInput, "Please select a gender.");
            return false;
        }
        return true;
    }
    // Required fields check before submission
    function requiredCheck() {
        const requiredFields = [
            "id_name_title",
            "id_first_name",
            "id_dob",
            "id_gender"
        ];
        
        let formIsValid = true;
        requiredFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            clearError(field);
            if (field && !field.value.trim()) {
                showError(field, "This field is required.");
                formIsValid = false;
            }
        });
        return formIsValid;
    }
    function validateDateOfBirth() {
        const dobInput = document.getElementById("id_dob"); // Assuming "id_dob" is the ID for the date of birth field
        clearError(dobInput);

        const dobValue = dobInput.value.trim();
        if (dobValue === "") {
            showError(dobInput, "Date of Birth is required.");
            return false;
        }

        const dob = new Date(dobValue);
        const today = new Date();
        
        // Calculate the user's age
        const age = today.getFullYear() - dob.getFullYear();
        const monthDiff = today.getMonth() - dob.getMonth();
        const dayDiff = today.getDate() - dob.getDate();
        
        // Adjust age if today's month and day are before the birth date month and day
        const adjustedAge = monthDiff > 0 || (monthDiff === 0 && dayDiff >= 0) ? age : age - 1;

        if (adjustedAge < 14) {
            showError(dobInput, "You must be at least 14 years old.");
            return false;
        }

        return true;
    }


    function validateBio() {
        const bioInput = document.getElementById("id_bio");
        const bio = bioInput.value.trim();
        clearError(bioInput);

        
        if (bio.length > 1500) {
            showError(bioInput, "Bio cannot exceed 1500 characters.");
            return false;
        }
        return true;
    }

    function validateProfilePicture() {
        const profilePictureInput = document.querySelector("input[name='profile_picture']");
        clearError(profilePictureInput);

        if (profilePictureInput.files.length > 0) {
            const file = profilePictureInput.files[0];
            const allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;
            const maxSize = 5 * 1024 * 1024; // 5MB

            if (!allowedExtensions.exec(file.name)) {
                
                showError(document.querySelector('.image-upload-container'), "Only .jpg, .jpeg, and .png files are allowed.");
                profilePictureInput.value = ""; // Clear invalid file
                return false;
            }

            if (file.size > maxSize) {
                showError(document.querySelector('.image-upload-container'), "File size must be less than 5MB.");
                profilePictureInput.value = ""; // Clear invalid file
                return false;
            }
        }
        return true;
    }

    function validateBloodGroup() {
        const bloodGroupInput = document.getElementById("id_blood_group");
        clearError(bloodGroupInput);

        if (!bloodGroupInput.value) {
            showError(bloodGroupInput, "Blood group is required.");
            return false;
        }
        return true;
    }

    async function checkAvailability(username) {
        let response = await fetch(`/accounts/api/check-username/?username=${username}`);
        let data = await response.json();
        return data.exists;
    }

    // Validation function for username
    function validateUsername() {
        const usernameInput = document.getElementById("id_username");
        const username = usernameInput.value.trim();
        clearError(usernameInput);

        if (username === "") {
            showError(usernameInput, "Username is required.");
            return false;
        }

        // Django's username regex
        const usernameRegex = /^[\w.@+-]+$/;
        if (!usernameRegex.test(username)) {
            showError(usernameInput, "Username can only contain letters, numbers, and @/./+/-/_ characters.");
            return false;
        }

        // Check if username already exists
        checkAvailability(username).then((exists) => {
            if (exists) {
                showError(usernameInput, "Username already exists.");
            }
        });

        return true;
    }

    // Field validation functions
    function validateOldPassword() {
        const oldPasswordInput = document.getElementById("id_old_password");
        const oldPassword = oldPasswordInput.value.trim();
        clearError(oldPasswordInput);

        if (oldPassword === "") {
            showError(oldPasswordInput, "Old password is required.");
            return false;
        }
        return true;
    }

    function validateNewPassword1() {
        const newPassword1Input = document.getElementById("id_new_password1");
        const newPassword1 = newPassword1Input.value.trim();
        clearError(newPassword1Input);

        if (newPassword1 === "") {
            showError(newPassword1Input, "New password is required.");
            return false;
        }

        if (newPassword1.length < 6) {
            showError(newPassword1Input, "Password must be at least 6 characters.");
            return false;
        }

        // const passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).+$/;
        // if (!passwordRegex.test(newPassword1)) {
        //     showError(newPassword1Input, "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.");
        //     return false;
        // }
        return true;
    }

    function validateNewPassword2() {
        const newPassword1Input = document.getElementById("id_new_password1");
        const newPassword2Input = document.getElementById("id_new_password2");
        clearError(newPassword2Input);

        if (newPassword2Input.value.trim() === "") {
            showError(newPassword2Input, "Please confirm the new password.");
            return false;
        }

        if (newPassword2Input.value !== newPassword1Input.value) {
            showError(newPassword2Input, "Passwords do not match.");
            return false;
        }
        return true;
    }

    function validateChangeEmail() {
        const emailInput = document.getElementById('new_email');
        const email = emailInput.value.trim();
        clearError(emailInput);
        
        if (email === "") {
            showError(emailInput, "Email is required.");
            return false;
        }

        const emailRegex = /^[\w.%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/i;
        if (!emailRegex.test(email)) {
            showError(emailInput, "Invalid email format.");
            return false;
        }

        // Check if email already exists
        checkAvailability("email", email, "check-email").then((exists) => {
            if (exists) {
                showError(emailInput, "Email already exists.");
            }
        });

        return true;
    }


    // Form submission validation
   

    // document.getElementById("id_phone_prefix").addEventListener("focusout", validatePhonePrefix) 
    // document.getElementById("id_phone_number").addEventListener("focusout", validatePhoneNumber)
    // document.getElementById("id_email").addEventListener("focusout", validateEmail)
    document.getElementById("id_address").addEventListener("focusout", validateAddress)
    document.getElementById("id_country").addEventListener("focusout", validateCountry)
    document.getElementById("id_state").addEventListener("focusout", validateState)
    document.getElementById("id_city").addEventListener("focusout", validateCity)
    document.getElementById("id_postal_code").addEventListener("focusout", validatePostalCode)
    document.getElementById("id_dob").addEventListener("change", validateDateOfBirth);
    document.getElementById("id_name_title").addEventListener("focusout", validateNameTitle);
    document.getElementById("id_first_name").addEventListener("focusout", validateFirstName);
    document.getElementById("id_last_name").addEventListener("focusout", validateLastName);
    document.getElementById("id_dob").addEventListener("focusout", validateDOB);
    document.getElementById("id_gender").addEventListener("focusout", validateGender);
    document.getElementById("id_instagram_link").addEventListener("focusout", validateInstagram);
    document.getElementById("id_twitter_link").addEventListener("focusout", validateTwitter);
    document.getElementById("id_linkedin_link").addEventListener("focusout", validateLinkedIn);
    document.getElementById("id_facebook_link").addEventListener("focusout", validateFacebook);
    document.getElementById("id_instagram_link").addEventListener("keypress", validateInstagram);
    document.getElementById("id_twitter_link").addEventListener("keypress", validateTwitter);
    document.getElementById("id_linkedin_link").addEventListener("keypress", validateLinkedIn);
    document.getElementById("id_facebook_link").addEventListener("keypress", validateFacebook);


    document.getElementById("id_bio").addEventListener("focusout", validateBio);
    document.querySelector("input[name='profile_picture']").addEventListener("change", validateProfilePicture);
    document.getElementById("id_blood_group").addEventListener("focusout", validateBloodGroup);

    document.getElementById("id_username").addEventListener("focusout", validateUsername);

    document.getElementById("id_old_password").addEventListener("focusout", validateOldPassword);
    document.getElementById("id_new_password1").addEventListener("focusout", validateNewPassword1);
    document.getElementById("id_new_password2").addEventListener("focusout", validateNewPassword2);
    
    document.getElementById("new_email").addEventListener("focusout", validateChangeEmail);
    document.getElementById("id_occupation_detail").addEventListener("focusout", validateOccupation)
