document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('order-form');
  const url = form.dataset.url;
  const overlay = document.getElementById('overlay');
//  const responseMessage = document.getElementById('response-message');
  const responseMessageError = document.getElementById('response-message-error');

  // обработчик submit только один раз
  if (!form.dataset.handlerAttached) {
    form.addEventListener('submit', (e) => {
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
      .then(res => {
        if (!res.ok) throw new Error('Введите Ваши данные корректно');
        return res.json();
      })
      .then(data => {
        alert('✅ Заказ успешно создан!');
        form.reset();
        overlay.classList.remove('active');
        form.classList.remove('active');

        // очистка корзины глобально
        if (window.basket) {
          window.basket = {};
          saveBasketToCookies({});
          const basketContainer = document.getElementById('basket');
          basketContainer.innerHTML = '<p>Корзина пуста.</p>';
        }
      })
      .catch(err => {
        responseMessageError.innerText = err.message;
      });
    });

    form.dataset.handlerAttached = 'true';
  }

  // клик по overlay для закрытия модалки
  overlay.addEventListener('click', () => {
    overlay.classList.remove('active');
    form.classList.remove('active');
  });
});