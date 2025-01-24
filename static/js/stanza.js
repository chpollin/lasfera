// Handle toggling line codes
document.addEventListener("DOMContentLoaded", (event) => {
  const lineCodeDisplay = document.getElementById("lineCodeDisplay");
  console.log("Select element:", lineCodeDisplay); // Debug line
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
