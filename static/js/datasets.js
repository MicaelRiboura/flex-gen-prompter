const dropzone = document.getElementById('dropzoneDataset');
const fileInput = document.getElementById('fileInput');
const message = document.getElementById('message');
const cardDatasetFile = document.getElementById('cardDatasetFile');

dropzone.addEventListener('click', () => fileInput.click());

dropzone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropzone.classList.add('dragover');
});

dropzone.addEventListener('dragleave', () => {
  dropzone.classList.remove('dragover');
});

dropzone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropzone.classList.remove('dragover');
  const file = e.dataTransfer.files[0];
  if (file) {
    dropzone.style.display = 'none';
    cardDatasetFile.classList.remove('hidden');
    cardDatasetFile.classList.add('flex');
    cardDatasetFile.querySelector('p')
      .innerText = file.name;
  }
  else {
    dropzone.style.display = 'flex';
  }
});

fileInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) {
    dropzone.style.display = 'none';
    cardDatasetFile.classList.remove('hidden');
    cardDatasetFile.classList.add('flex');
    cardDatasetFile.querySelector('p')
      .innerText = file.name;
  }
  else {
    dropzone.style.display = 'flex';
  }
});

document.getElementById('btnImportDataset').addEventListener('click', () => {
  const file = fileInput.files[0];
  if (file) {
    uploadFile(file);
    dropzone.style.display = 'flex';
    cardDatasetFile.classList.add('hidden');
    cardDatasetFile.classList.remove('flex');
    window.location.reload();
  }
});

function uploadFile(file) {
  if (!file.name.endsWith('.csv')) {
    message.textContent = '❌ Apenas arquivos CSV são permitidos.';
    return;
  }

  const formData = new FormData();
  formData.append('file', file);

  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/upload/', true);
  xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

  xhr.onload = function () {
    if (xhr.status === 200) {
      const response = JSON.parse(xhr.responseText);
      message.textContent = `✅ ${response.message}`;
    } else {
      message.textContent = `❌ Upload falhou!`;
    }
  };

  xhr.onerror = function () {
    message.textContent = '❌ Um erro ocorreu durante o upload.';
  };

  xhr.send(formData);
}

// Helper to get CSRF token (Django)
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}