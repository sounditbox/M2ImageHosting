const tabLinks = document.querySelectorAll('.tab-link');
const tabContents = document.querySelectorAll('.tab-content');

tabLinks.forEach((link) => {
  link.addEventListener('click', () => {
    tabLinks.forEach((item) => item.classList.remove('active'));
    tabContents.forEach((content) => content.classList.remove('active'));

    link.classList.add('active');
    const tabId = link.getAttribute('data-tab');
    document.getElementById(tabId).classList.add('active');
  });
});

const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('fileInput');
const browseButton = document.getElementById('browseButton');
const uploadUrlInput = document.getElementById('uploadUrl');
const copyButton = document.getElementById('copyButton');

browseButton.addEventListener('click', () => {
  fileInput.click();
});

dropArea.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropArea.classList.add('dragover');
});

dropArea.addEventListener('dragleave', () => {
  dropArea.classList.remove('dragover');
});

dropArea.addEventListener('drop', (e) => {
  e.preventDefault();
  dropArea.classList.remove('dragover');
  const files = e.dataTransfer.files;
  if (files.length) {
    handleFiles(files);
  }
});

fileInput.addEventListener('change', () => {
  handleFiles(fileInput.files);
});

function handleFiles(files) {
  const file = files[0];
  if (!file) return;

  if (!['image/jpeg','image/png','image/gif', 'image/jpg'].includes(file.type)) {
    // Ошибка
    dropArea.classList.add('error');
    dropArea.classList.remove('success');
    return;
  }

  if (file.size > 5 * 1024 * 1024) {
    dropArea.classList.add('error');
    dropArea.classList.remove('success');
    return;
  }

  dropArea.classList.remove('error');

  simulateUpload(file)
    .then((url) => {
      dropArea.classList.add('success');
      uploadUrlInput.value = url;
    })
    .catch(() => {
      dropArea.classList.add('error');
    });
}

function simulateUpload(file) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve('https://sharefile.xyz/myfile.jpg');
    }, 1500);
  });
}

copyButton.addEventListener('click', () => {
  navigator.clipboard.writeText(uploadUrlInput.value)
    .then(() => {
      alert('Link copied to clipboard!');
    })
    .catch((err) => {
      console.error('Failed to copy:', err);
    });
});

fileInput.addEventListener('change', () => {
  const file = fileInput.files[0];
  if (!file) return alert('Выберите файл для загрузки.');

  fetch('/api/upload/', {
    method: 'POST',
    headers: {
      'Filename': file.name
    },
    body: file
  })
  .then(response => response.text())
  .then(html => {
    document.getElementById('uploadResult').innerHTML = html;
  })
  .catch(error => {
    console.error('Ошибка загрузки:', error);
  });
});

//     fetch('/api/images').then(response => response.json()).then(images => setImages(images.images));

//    function setImages(images) {
//        const imagesContainer = document.createElement('div');
//        images.forEach(image => {
//            const imageElement = document.createElement('img');
//            imageElement.src = `/images/${image}`;
//            imagesContainer.appendChild(imageElement);
//        });
//        document.body.appendChild(imagesContainer);
//    }