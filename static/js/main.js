document.addEventListener('DOMContentLoaded', () => {
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('file-input');
  const previewContainer = document.getElementById('preview-container');
  const dropzonePrompt = document.getElementById('dropzone-prompt');
  const imagePreview = document.getElementById('image-preview');
  const previewFilename = document.getElementById('preview-filename');
  const uploadForm = document.getElementById('upload-form');
  const submitBtn = document.getElementById('submit-btn');

  if (dropzone && fileInput) {
    // Click to open file dialog
    dropzone.addEventListener('click', () => {
      fileInput.click();
    });

    // Drag over styling
    ['dragenter', 'dragover'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.add('active');
      });
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.remove('active');
      });
    });

    // Drop file
    dropzone.addEventListener('drop', (e) => {
      const files = e.dataTransfer.files;
      if (files.length > 0) {
        fileInput.files = files;
        handleFileSelect(files[0]);
      }
    });

    // Change event from browse
    fileInput.addEventListener('change', () => {
      if (fileInput.files.length > 0) {
        handleFileSelect(fileInput.files[0]);
      }
    });
  }

  function handleFileSelect(file) {
    if (!file.type.startsWith('image/')) {
      alert('Please upload a valid histopathology image file (PNG, JPG, TIFF).');
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.src = e.target.result;
      previewFilename.textContent = file.name;
      dropzonePrompt.style.display = 'none';
      previewContainer.style.display = 'block';
    };
    reader.readAsDataURL(file);
  }

  if (uploadForm && submitBtn) {
    uploadForm.addEventListener('submit', () => {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '⚡ Analyzing Deep Learning Features & Grad-CAM...';
    });
  }
});

