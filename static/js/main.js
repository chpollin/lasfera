document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".dropdown-toggle").forEach((button) => {
    button.addEventListener("click", function () {
      const dropdown = this.nextElementSibling;
      const isOpen = !dropdown.classList.contains("hidden");
      document
        .querySelectorAll("nav .relative ul")
        .forEach((ul) => ul.classList.add("hidden"));
      document
        .querySelectorAll(".dropdown-toggle")
        .forEach((btn) => btn.classList.remove("dropdown-open"));

      if (!isOpen) {
        dropdown.classList.remove("hidden");
        this.classList.add("dropdown-open");
      }
    });
  });

  document.addEventListener("click", function (e) {
    if (!e.target.closest("nav")) {
      document
        .querySelectorAll("nav .relative ul")
        .forEach((ul) => ul.classList.add("hidden"));
      document
        .querySelectorAll(".dropdown-toggle")
        .forEach((btn) => btn.classList.remove("dropdown-open"));
    }
  });
});
