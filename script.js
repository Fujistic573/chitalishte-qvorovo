// This code makes elements with the class "fade-in" appear as you scroll.

const observer = new IntersectionObserver((entries) => {
    // Loop over the entries
    entries.forEach((entry) => {
        // If the element is visible
        if (entry.isIntersecting) {
            // Add the 'visible' class to it
            entry.target.classList.add('visible');
        }
    });
});

// Get all the elements you want to animate
const fadeInElements = document.querySelectorAll('.fade-in');

// Tell the observer to watch each of them
fadeInElements.forEach((el) => observer.observe(el));