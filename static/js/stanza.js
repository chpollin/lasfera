// Handle toggling line codes
document.addEventListener("DOMContentLoaded", (event) => {
  const lineCodeDisplay = document.getElementById("lineCodeDisplay");
  if (lineCodeDisplay) {
    let originalLineCodes = [];
    let lineCodesVisible = true;

    lineCodeDisplay.addEventListener("change", function () {
      const lineCodes = document.querySelectorAll(".line-code");
      const lineCodeLinks = document.querySelectorAll(".line-code a");

      switch (this.value) {
        case "full":
          // Show full line codes
          lineCodes.forEach((code) => (code.style.display = "inline"));
          if (originalLineCodes.length) {
            lineCodeLinks.forEach((link, i) => {
              link.querySelector("span").textContent = originalLineCodes[i];
            });
          }
          break;

        case "shortened":
          // Show shortened line codes
          lineCodes.forEach((code) => (code.style.display = "inline"));
          lineCodeLinks.forEach((link, i) => {
            const span = link.querySelector("span");
            if (!originalLineCodes[i]) {
              originalLineCodes[i] = span.textContent;
            }
            const parts = span.textContent.split(".");
            span.textContent = parseInt(parts[parts.length - 1]);
          });
          break;

        case "hidden":
          // Hide line codes
          lineCodes.forEach((code) => (code.style.display = "none"));
          break;
      }
    });
  }
});

// Return to top button
window.addEventListener("scroll", function () {
  const returnToTop = document.getElementById("return-to-top");
  if (!returnToTop) return;
  
  const top = document.getElementById("top");
  if (!top) return;
  
  const distanceFromTop = top.getBoundingClientRect().top;

  // Show the button after the #top anchor is 100px above the viewport
  if (distanceFromTop < -100) {
    returnToTop.classList.remove("opacity-0", "invisible");
    returnToTop.classList.add("opacity-100");
  } else {
    returnToTop.classList.remove("opacity-100");
    returnToTop.classList.add("opacity-0", "invisible");
  }
});

// Function to update the line code display
function updateLineCodeDisplay(mode) {
  const lineCodes = document.querySelectorAll('.line-code');
  lineCodes.forEach(code => {
    switch(mode) {
      case 'shortened':
        // Show only last part of line code (e.g., "01" from "01.01.01")
        const shortCode = code.textContent.trim().split('.').pop();
        code.style.display = '';
        code.querySelector('span').textContent = shortCode;
        break;
      case 'hidden':
        code.style.display = 'none';
        break;
      default: // 'full'
        code.style.display = '';
        // Restore original line code if needed
        const originalCode = code.querySelector('a').id;
        code.querySelector('span').textContent = originalCode;
    }
  });
}
