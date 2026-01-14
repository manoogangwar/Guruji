
    const texts = ["Discover the Haidakhandi universe.","Search through over 200,000 members worldwide.","Explore spirituality.", "Connect with Haidakhandi.","Connect with a global community of 200,000+ Haidakhandis" ,"Discover a new journey.","Explore Haidakhandi connections worldwide.","Find your spiritual network among 200k+ Haidakhandis around"];
    const typingSpeed = 100; // Speed of typing in ms
    const erasingSpeed = 50; // Speed of erasing in ms
    const delayBetweenTexts = 1000; // Delay before starting next text in ms

    const typingTextDiv = document.getElementById("typing-text");
    let currentTextIndex = 0;
    let charIndex = 0;
    let isErasing = false;
if(typingTextDiv){
    function typeText() {
      const currentText = texts[currentTextIndex];
      
      if (!isErasing) {
        // Typing effect
        typingTextDiv.textContent = currentText.substring(0, charIndex + 1);
        charIndex++;

        if (charIndex === currentText.length) {
          // When typing is done, wait and start erasing
          setTimeout(() => isErasing = true, delayBetweenTexts);
        }
      } else {
        // Erasing effect
        typingTextDiv.textContent = currentText.substring(0, charIndex - 1);
        charIndex--;

        if (charIndex === 0) {
          // When erasing is done, move to the next text
          isErasing = false;
          currentTextIndex = (currentTextIndex + 1) % texts.length;
        }
      }

      // Recursively call typeText with delay
      setTimeout(typeText, isErasing ? erasingSpeed : typingSpeed);
    }

    // Start the typing effect
    typeText();
}
