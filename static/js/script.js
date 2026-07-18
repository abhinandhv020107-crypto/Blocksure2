document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-copy]").forEach((button) => {
    button.addEventListener("click", () => navigator.clipboard.writeText(button.dataset.copy || ""));
  });

  document.querySelectorAll("[data-scanner-button]").forEach((button) => {
    button.addEventListener("click", () => {
      alert("Camera scanner UI is ready. The QR scanner module will connect here during integration.");
    });
  });
});
