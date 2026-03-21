const previewImg = document.getElementById("previewImg");
const resultImg = document.getElementById("resultImg");
const statusText = document.getElementById("status");

document.getElementById("fileInput").addEventListener("change", function () {
    const file = this.files[0];

    if (file) {
        previewImg.src = URL.createObjectURL(file);
        resultImg.src = ""; // clear old result
        statusText.innerHTML = "📄 Image ready for evaluation";
    }
});

function uploadImage() {
    const fileInput = document.getElementById("fileInput");

    if (fileInput.files.length === 0) {
        alert("Please select an image");
        return;
    }

    statusText.innerHTML = "⏳ Evaluating...";

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData
    })
    .then(res => res.blob())
    .then(data => {
        resultImg.src = URL.createObjectURL(data);
        statusText.innerHTML = "✅ Evaluated";
    })
    .catch(err => {
        console.error(err);
        statusText.innerHTML = "❌ Error";
    });
}