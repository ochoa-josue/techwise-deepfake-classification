function uploadImage() {
  const input = document.getElementById('imageInput');
  const resultDiv = document.getElementById('result');
  
  if (input.files && input.files.length > 0) {
      const formData = new FormData();
      // Append each file to the form data
      for (const file of input.files) {
          formData.append('image', file, file.name);
      }

      // Adjust the fetch URL as needed
      fetch('http://127.0.0.1:8000/upload', {
          method: 'POST',
          body: formData,
      })
      .then(response => response.json())
      .then(data => {
          console.log(data); // You'll need to adjust how you want to display the array of results
          resultDiv.innerHTML = data.map(item => {
              if (item.error) {
                  return `<p style="color: red;">${item.filename}: Error - ${item.error}</p>`;
              } else {
                  return `<p style="color: green;">${item.filename}: Is Deepfake - ${item.is_deepfake}</p>`;
              }
          }).join('');
      })
      .catch(error => {
          console.error(error);
          resultDiv.innerHTML = `<p style="color: red;">Error processing the images.</p>`;
      });
  } else {
      resultDiv.innerHTML = `<p style="color: red;">Please select at least one image file.</p>`;
  }
}

// This function updates the file name text
function updateFileName() {
  const input = document.getElementById("imageInput");
  const fileName = input.files[0] ? input.files[0].name : "No file chosen";
  document.getElementById("file-name").textContent = fileName;
}