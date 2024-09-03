function showSection(sectionId) {
  const sections = document.querySelectorAll('.section');
  sections.forEach(section => {
      section.classList.remove('active');
  });
  document.getElementById(sectionId).classList.add('active');

  const links = document.querySelectorAll('.sidebar a');
  links.forEach(link => {
      link.classList.remove('active');
  });
  document.querySelector(`.sidebar a[href="#${sectionId}"]`).classList.add('active');
}

function previewImage(event) {
  const preview = document.getElementById('image-preview-src');
  preview.src = URL.createObjectURL(event.target.files[0]);
  preview.style.display = 'block';
}

function resetImagePreview() {
  const preview = document.getElementById('image-preview-src');
  preview.src = '#';
  preview.style.display = 'none';
}
function previewLogo(event) {
  const preview = document.getElementById('logo-preview-src');
  preview.src = URL.createObjectURL(event.target.files[0]);
  preview.style.display = 'block';
}

function resetLogoPreview() {
  const preview = document.getElementById('logo-preview-src');
  preview.src = '#';
  preview.style.display = 'none';
}

function showOverlay(message, onConfirm, onCancel) {
  const overlay = document.createElement('div');
  overlay.className = 'overlay';
  overlay.innerHTML = `
      <div class="confirmation-box">
          <p>${message}</p>
          <button id="confirm-btn">Confirm</button>
          <button id="cancel-btn">Cancel</button>
      </div>
  `;
  document.body.appendChild(overlay);

  setTimeout(() => overlay.classList.add('active'), 10);

  document.getElementById('confirm-btn').addEventListener('click', () => {
      onConfirm();
      closeOverlay(overlay);
  });

  document.getElementById('cancel-btn').addEventListener('click', () => {
      onCancel();
      closeOverlay(overlay);
  });
}

function closeOverlay(overlay) {
  overlay.classList.remove('active');
  setTimeout(() => overlay.remove(), 300);
}

document.querySelectorAll('form').forEach(form => {
  form.addEventListener('submit', (e) => {
      e.preventDefault();
      showOverlay(
          'Are you sure you want to save these changes?',
          () => {
              console.log('Changes saved');
              // Add code to save changes
          },
          () => console.log('Save cancelled')
      );
  });

  form.addEventListener('reset', (e) => {
      e.preventDefault();
      showOverlay(
          'Are you sure you want to reset this form?',
          () => {
              console.log('Form reset');
              form.reset();
              if (form.id === 'logo-form') {
                  resetLogoPreview();
              }
          },
          () => console.log('Reset cancelled')
      );
  });
});
document.getElementById('role-select').addEventListener('change', function() {
document.getElementById('selected-role').textContent = this.options[this.selectedIndex].text;
});

document.getElementById('password-policy').addEventListener('change', function() {
const customPolicy = document.getElementById('custom-password-policy');
customPolicy.style.display = this.value === 'custom' ? 'block' : 'none';
});