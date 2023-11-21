

document.addEventListener('DOMContentLoaded', function () {
    
    // Function to show the overlay
    function showOverlay() {
        console.log("A");
        document.getElementById("overlay").style.display = "block";
    }

    // Function to hide the overlay
    function hideOverlay() {
        console.log("B");
        document.getElementById("overlay").style.display = "none";
    }

    // Attach the functions to the form submission
    const mainForm = document.querySelector('form');

    if (mainForm) {
        mainForm.addEventListener('submit', function () {
            showOverlay();
        });
    } else {
        console.error('Main form not found');
    }

    const appendForm = document.querySelector('#appendForm');

    if (appendForm) {
        appendForm.addEventListener('submit', function () {
            showOverlay();
        });
    } else {
        console.error('Form with id "appendForm" not found');
    }
});
