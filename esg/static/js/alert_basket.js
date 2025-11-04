(function() {
  const alertBox = document.getElementById('custom-alert');
  const alertMessage = document.getElementById('custom-alert-message');
  const alertBtn = document.getElementById('custom-alert-btn');

  window.alert = function(message) {
    alertMessage.textContent = message;
    alertBox.classList.add('active');

    // скрыть автоматически через 3 сек
    setTimeout(() => {
      alertBox.classList.remove('active');
    }, 3000);
  };

  // кнопка "OK"
  alertBtn.addEventListener('click', () => {
    alertBox.classList.remove('active');
  });
})();