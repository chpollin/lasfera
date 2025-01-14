// Handle toggling line codes
document.addEventListener("DOMContentLoaded", (event) => {
  const toggleLineCodes = document.getElementById("toggleLineCodes");
  if (toggleLineCodes) {
    toggleLineCodes.addEventListener("click", function () {
      const lineCodes = document.querySelectorAll(".line-code");
      lineCodes.forEach((lineCode) => {
        lineCode.style.display = this.checked ? "inline" : "none";
      });
    });
  }
});

// Handle shortening the line codes
// We shorten the code from 01.01.01 to 1 (that is, the final .01)
document.addEventListener("DOMContentLoaded", (event) => {
  const shortenLineCodes = document.getElementById("toggleLineCodeShortened");

  if (shortenLineCodes) {
    let originalLineCodes = [];

    shortenLineCodes.addEventListener("click", function () {
      const lineCodeLinks = document.querySelectorAll(".line-code a");

      for (let i = 0; i < lineCodeLinks.length; i++) {
        const lineCodeSpan = lineCodeLinks[i].querySelector("span");
        if (this.checked) {
          // Save the original line code
          originalLineCodes[i] = lineCodeSpan.textContent;

          // Shorten the line code
          let code = lineCodeSpan.textContent;
          let parts = code.split(".");
          let lastPart = parts[parts.length - 1];
          lineCodeSpan.textContent = parseInt(lastPart);
        } else {
          // Restore the original line code
          if (originalLineCodes.length) {
            lineCodeSpan.textContent = originalLineCodes[i];
          }
        }
      }
    });
  }
});

// Return to top button
window.addEventListener("scroll", function () {
  const returnToTop = document.getElementById("return-to-top");
  const top = document.getElementById("top");
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

// Manuscript viewer
document.addEventListener("DOMContentLoaded", function () {
  const manuscriptSelect = document.getElementById("manuscript-select");
  const miradorFrame = document.getElementById("mirador-frame");

  if (manuscriptSelect && miradorFrame) {
    manuscriptSelect.addEventListener("change", function () {
      const manuscriptId = this.value; // This will now be the numeric ID

      // Update the iframe source to load the new manuscript
      if (manuscriptId) {
        const currentUrl = new URL(miradorFrame.src);
        const newUrl = currentUrl.pathname.replace(
          /\/\d+\/0001/,
          `/${manuscriptId}/0001`,
        );
        miradorFrame.src = newUrl;
      }
    });
  }
});
