document.addEventListener("DOMContentLoaded", function() {
    console.log("JavaScript loaded successfully!");


    let uploadForm = document.querySelector("form");
    if (uploadForm) {
        uploadForm.addEventListener("submit", function() {
            alert("Image is being uploaded and processed...");
        });
    }
});
