document.addEventListener('DOMContentLoaded', () => {
  const overlay = document.getElementById('overlay');
  const modal = document.getElementById('order-form');
  const closeBtn = document.getElementById('close-order-form');

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
    }, 300); // плавное скрытие
  };

  // ловим клик по кнопке "Оформить заказ" из basket.js
  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('open-order-form')) {
      e.preventDefault();
      openModal();
    }
  });

  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  overlay.addEventListener('click', closeModal);
});
