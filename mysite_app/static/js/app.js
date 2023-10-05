document.addEventListener("DOMContentLoaded", function () {
    function toggleMenu() {
        var menu = document.querySelector(".nav-menu");
        menu.classList.toggle("show");
      }
  });


  console.log("Script is running...");
  // app.js

document.addEventListener("DOMContentLoaded", function () {


  // Load the animation
  var animation = bodymovin.loadAnimation({
      container: document.getElementById("email-animation"),
      renderer: "svg", // You can use "canvas" or "html" as well
      loop: true, // Set to true if you want the animation to loop
      autoplay: true, // Set to true if you want the animation to play automatically
      path: '/static/lotties/email-animation.json', // Path to your Lottie JSON file
  });

      bodymovin.loadAnimation({
      container: document.getElementById('cold-email-animation'),
      renderer: 'svg',
      loop: true,
      autoplay: true,
      path: '/static/lotties/cold-email-automation-orange.json'
    });
  
      bodymovin.loadAnimation({
      container: document.getElementById('email-verification-animation'),
      renderer: 'svg',
      loop: true,
      autoplay: true,
      path: '/static/lotties/email-verification-orange.json'
    });

});
