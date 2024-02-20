function uploadImage() {
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("image", file);

    return fetch("/upload", {
        method: "POST",
        body: formData,
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then((data) => {
        console.log("Success:", data);
        if (data.result !== undefined) {
            alert("Upload Success: " + data.result);
        } else {
            alert("Upload Failed: " + data.error);
        }
    })
    .catch((error) => {
        console.error("Error:", error);
        alert("Upload Failed");
    });
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('fileInput').addEventListener('change', uploadImage);
});
