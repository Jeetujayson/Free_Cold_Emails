document.addEventListener('DOMContentLoaded', function () {
    // Function to show the overlay
    function showOverlay() {
        document.getElementById("overlay").style.display = "block";
    }

    // Function to hide the overlay
    function hideOverlay() {
        document.getElementById("overlay").style.display = "none";
    }

    // Attach the functions to the form submission
    document.querySelector('form').addEventListener('submit', function () {
        showOverlay();
    });
});



