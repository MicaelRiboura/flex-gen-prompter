const dropzone = document.getElementById('dropzoneDataset');
const fileInput = document.getElementById('fileInput');
const message = document.getElementById('message');
const cardDatasetFile = document.getElementById('cardDatasetFile');

function renderDatasetsTable() {
  fetch('/datasets-data/')
    .then(response => response.json())
    .then(data => {
      const tableBody = document.getElementById('datasets-table').querySelector('tbody');
      let rows = [];
      if (data?.datasets && data?.datasets.length != 0) {
        rows = data.datasets.map(dataset => {
          return `
              <tr class="bg-white border-b border-gray-200">
                    <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">
                        ${dataset}
                    </th>
                    <td class="px-6 py-4 text-blue-600 text-lg hover:text-blue-800">
                        <a href="/datasets/${dataset}/">
                            <i class="fa-solid fa-eye cursor-pointer"></i>
                        </a>
                    </td>
                </tr>
          `;
        });
      } else {
        rows = [`
            <tr class="bg-white">
                <th colspan="2" scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">
                    Nenhum dataset disponível.
                </th>
            </tr>
        `];
      }

      tableBody.innerHTML = rows.join('');
    });
}

document.addEventListener('DOMContentLoaded', () => {
  renderDatasetsTable();
});

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

  fileInput.files = e.dataTransfer.files;
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
      document.getElementById('importDatasetModal').classList.add('hidden');
      setTimeout(() => {
        renderDatasetsTable();
      }, 500);
    } else {
      const response = JSON.parse(xhr.responseText);
      message.textContent = '❌ ' + response.error || '❌ Um erro ocorreu durante o upload.';
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