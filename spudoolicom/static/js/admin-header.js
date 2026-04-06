(function () {
  const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
  const fileInput = document.getElementById('file-input');
  const uploadWrap = document.getElementById('upload-wrap');
  const uploadStatus = document.getElementById('upload-status');
  const cropperWrap = document.getElementById('cropper-wrap');
  const cropperImage = document.getElementById('cropper-image');
  const saveBtn = document.getElementById('save-btn');
  const resetBtn = document.getElementById('reset-btn');
  const statusMsg = document.getElementById('status-msg');
  let cropper = null;

  fileInput.addEventListener('change', async function () {
    const file = fileInput.files[0];
    if (!file) return;
    uploadStatus.textContent = 'Uploading…';

    const fd = new FormData();
    fd.append('file', file);

    const resp = await fetch('/admin/header/upload', {
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken },
      body: fd
    });
    const data = await resp.json();

    if (!resp.ok || data.error) {
      uploadStatus.textContent = 'Upload failed: ' + (data.error || resp.statusText);
      return;
    }

    // Bust cache so the browser loads the newly uploaded temp image
    cropperImage.src = data.url + '?t=' + Date.now();
    uploadWrap.style.display = 'none';
    cropperWrap.style.display = 'block';
    statusMsg.style.display = 'none';

    if (cropper) {
      cropper.destroy();
    }
    cropper = new Cropper(cropperImage, {
      aspectRatio: 1320 / 180,
      viewMode: 1,
      autoCropArea: 1,
      movable: true,
      zoomable: true,
      rotatable: false,
      scalable: false
    });
  });

  saveBtn.addEventListener('click', async function () {
    if (!cropper) return;
    const d = cropper.getData(true); // true = rounded integers
    saveBtn.disabled = true;
    saveBtn.textContent = 'Saving…';

    const resp = await fetch('/admin/header/save', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({ x: d.x, y: d.y, width: d.width, height: d.height })
    });
    const result = await resp.json();

    saveBtn.disabled = false;
    saveBtn.textContent = 'Save as header.jpg';
    statusMsg.style.display = 'block';

    if (resp.ok && result.ok) {
      statusMsg.className = 'alert alert-success';
      statusMsg.textContent = 'Header image saved successfully.';
    } else {
      statusMsg.className = 'alert alert-danger';
      statusMsg.textContent = 'Save failed: ' + (result.error || resp.statusText);
    }
  });

  resetBtn.addEventListener('click', function () {
    if (cropper) {
      cropper.destroy();
      cropper = null;
    }
    cropperWrap.style.display = 'none';
    uploadWrap.style.display = 'block';
    fileInput.value = '';
    uploadStatus.textContent = '';
  });
}());
