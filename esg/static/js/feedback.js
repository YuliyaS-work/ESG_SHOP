const overlay = document.getElementById('overlay_fb');
const modal = document.getElementById('feedback-modal');
const openBtn = document.getElementById('open-feedback');
const closeBtn = document.getElementById('close-feedback');
const form = document.getElementById('feedback-form');
const url = form.dataset.url;
const responseMessageError = document.getElementById('response-message-error_feedback');

const openModal = () => {
  overlay.style.display = 'block';
  modal.style.display = 'block';
  overlay.classList.add('active');
  modal.classList.add('active');
};

const closeModal = () => {
  overlay.classList.remove('active');
  modal.classList.remove('active');
  setTimeout(() => {
    overlay.style.display = 'none';
    modal.style.display = 'none';
  }, 300);
};

if (openBtn && modal && overlay) {
  openBtn.addEventListener('click', (e) => {
    e.preventDefault();
    openModal();
  });

  closeBtn.addEventListener('click', closeModal);
  overlay.addEventListener('click', closeModal);
}

// Обработка отправки формы
form.addEventListener('submit', function(e) {
  e.preventDefault();

  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken(), // Функция должна быть определена отдельно
    },
    body: JSON.stringify(data)
  })
  .then(response => {
    if (!response.ok) throw new Error('Что-то пошло не так. Проверьте  Ваши данные.');
    return response.json();
  })
  .then(data => {
    alert('☑️ Спасибо! Ваше сообщение отправлено.');
    responseMessageError.innerText = '';
    form.reset();
    closeModal();
  })
  .catch(error => {
    responseMessageError.innerText = error.message;
  });
});

function getCSRFToken() {
  return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}