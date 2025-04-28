document.addEventListener('DOMContentLoaded', function() {
    const loadingOverlay = document.getElementById('loadingOverlay');
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const newFolderBtn = document.getElementById('newFolderBtn');
  
    function showLoading() {
      loadingOverlay.style.display = 'flex';
    }
  
    function hideLoading() {
      loadingOverlay.style.display = 'none';
    }
  
    function uploadFiles(files) {
      if (!files.length) return;
      showLoading();
      const formData = new FormData();
      Array.from(files).forEach(file => {
        formData.append('file', file, file.webkitRelativePath || file.name);
      });
  
      fetch(window.location.pathname, {
        method: 'POST',
        body: formData
      })
      .then(() => location.reload())
      .catch(() => {
        alert('Erro ao enviar arquivos.');
        hideLoading();
      });
    }
  
    uploadArea.addEventListener('dragover', (e) => {
      e.preventDefault();
      uploadArea.classList.add('dragover');
    });
  
    uploadArea.addEventListener('dragleave', (e) => {
      e.preventDefault();
      uploadArea.classList.remove('dragover');
    });
  
    uploadArea.addEventListener('drop', (e) => {
      e.preventDefault();
      uploadArea.classList.remove('dragover');
      uploadFiles(e.dataTransfer.files);
    });
  
    fileInput.addEventListener('change', () => {
      uploadFiles(fileInput.files);
    });
  
    newFolderBtn.addEventListener('click', () => {
      const folderName = prompt('Nome da nova pasta:');
      if (folderName) {
        showLoading();
        const formData = new FormData();
        formData.append('new_folder', folderName);
  
        fetch(window.location.pathname, {
          method: 'POST',
          body: formData
        })
        .then(() => location.reload())
        .catch(() => {
          alert('Erro ao criar pasta.');
          hideLoading();
        });
      }
    });
  
    document.body.addEventListener('click', (e) => {
      if (e.target.closest('.deleteBtn')) {
        const path = e.target.closest('[data-path]').dataset.path;
        if (confirm('Deseja excluir?')) {
          showLoading();
          fetch(`/delete/${encodeURIComponent(path)}`, { method: 'POST' })
            .then(() => location.reload())
            .catch(() => {
              alert('Erro ao excluir.');
              hideLoading();
            });
        }
      }
    });
  });
  