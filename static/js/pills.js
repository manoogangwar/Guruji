$(document).ready(function() {
    $(window).keydown(function(event){
      if(event.keyCode == 13) {
        event.preventDefault();
        return false;
      }
    });
  });


document.addEventListener('DOMContentLoaded', function() {
    function addPill(inputField, pillContainer, value) {
        const pill = document.createElement('span');
        pill.classList.add('pill', 'badge', 'me-1');
        pill.textContent = value;
        
        const removeButton = document.createElement('a');
        removeButton.classList.add( 'ms-1','bi-x','text-white');
        removeButton.setAttribute('type', 'button');
        removeButton.addEventListener('click', () => {
            pillContainer.removeChild(pill);
            //updateInputField(inputField, pillContainer);
        });
        
        pill.appendChild(removeButton);
        pillContainer.appendChild(pill);
        //updateInputField(inputField, pillContainer);
    }

    function updateInputField(inputField, pillContainer) {
      const values = Array.from(pillContainer.querySelectorAll('.pill'))
                          .map(pill => pill.textContent.replace('×', '').trim());
      inputField.value = values.join(',');
  }

    function handleInputEvent(event, inputField, pillContainer) {
        if (event.key === 'Enter' || event.key === ',') {
            event.preventDefault();
            const value = inputField.value.trim();
            if (value) {
                addPill(inputField, pillContainer, value);
                inputField.value = '';
            }
        }
    }

    document.querySelectorAll('.pill-input').forEach(inputField => {
        const pillContainerId = inputField.getAttribute('data-pill-container');
        const pillContainer = document.getElementById(pillContainerId);
        
        if (inputField.value) {
            inputField.value.split(',').forEach(value => addPill(inputField, pillContainer, value.trim()));
            inputField.value = '';
        }

        inputField.addEventListener('keydown', event => handleInputEvent(event, inputField, pillContainer));
    });

    document.getElementById('member-profile-form').addEventListener('submit', function(event) {
      document.querySelectorAll('.pill-input').forEach(inputField => {
          const pillContainerId = inputField.getAttribute('data-pill-container');
          const pillContainer = document.getElementById(pillContainerId);
          updateInputField(inputField, pillContainer);
      });
      
  });
});