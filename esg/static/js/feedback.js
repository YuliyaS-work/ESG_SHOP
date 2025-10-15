const overlay = document.getElementById('overlay_fb');
const modal = document.getElementById('feedback-modal');
const openBtn = document.getElementById('open-feedback');
const closeBtn = document.getElementById('close-feedback');

const openModal = () => {
  overlay.style.display = 'block';
  modal.style.display = 'block';
  overlay.classList.add('active');
  modal.classList.add('active');
};

const closeModal = () => {
  overlay.classList.remove('active');
  modal.classList.remove('active');
};

if (openBtn && modal && overlay) {
  openBtn.addEventListener('click', (e) => {
    e.preventDefault();
    openModal();
  });

  closeBtn.addEventListener('click', closeModal);
  overlay.addEventListener('click', closeModal);
}