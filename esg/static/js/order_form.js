document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('order-form');
  const url = form.dataset.url;
  const overlay = document.getElementById('overlay');
  const responseMessage = document.getElementById('response-message');
  const responseMessageError = document.getElementById('response-message-error');

  form.addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
      body: JSON.stringify(data)
    })
    .then(response => {
      if (!response.ok) throw new Error('Введите Ваши данные корректно');
      return response.json();
    })
    .then(data => {
      responseMessage.innerText = '✅ Заказ успешно создан!';
      form.reset();
      form.style.display = 'none';
      overlay.style.display = 'none';

      saveBasketToCookies({});
      basket = {}; // Обновляем локальную переменную
      const basketContainer = document.getElementById('basket');
      basketContainer.innerHTML = '<p>Корзина пуста.</p>';
    })
    .catch(error => {
      responseMessageError.innerText = error.message;
    });
  });

  overlay.onclick = () => {
    form.style.display = 'none';
    overlay.style.display = 'none';
  };
});