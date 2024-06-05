// Get the sidebar, close button, and notation text elements
var sidebar = document.getElementById("sidebar");
var closeButton = document.getElementById("close-button");
var notationText = document.getElementById("notation-text");

// Listen for click events on the document
document.addEventListener("click", function (event) {
  // If the clicked element has a data-notation attribute
  if (event.target.hasAttribute("data-notation")) {
    // Get the data-notation text
    var text = event.target.getAttribute("data-notation");

    // Update the notation text
    notationText.textContent = text;

    // Show the sidebar
    sidebar.style.transform = "translateX(0)";
  }
});

// Add a click event listener to the close button
closeButton.addEventListener("click", function () {
  // Hide the sidebar
  sidebar.style.transform = "translateX(100%)";
});
