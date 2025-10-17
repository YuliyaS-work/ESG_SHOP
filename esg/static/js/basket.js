document.addEventListener('DOMContentLoaded', () => {
  const basketContainer = document.getElementById('basket');
  const form = document.getElementById('order-form');
  const overlay = document.getElementById('overlay');

  // глобальная корзина
  window.basket = getBasketFromCookies();

  function renderBasket() {
    basketContainer.innerHTML = '';
    const titles = Object.keys(window.basket);

    if (titles.length === 0) {
      basketContainer.innerHTML = '<p>Корзина пуста.</p>';
      return;
    }

    Object.entries(window.basket).forEach(([title, quantity]) => {
      const div = document.createElement('div');
      div.className = 'basket-item';
      div.innerHTML = `
        <span class="title">${title}</span>
        <button class="decrease">−</button>
        <span class="quantity">${quantity}</span>
        <button class="increase">+</button>
        <button class="remove">🗑️</button>
      `;
      div.querySelector('.increase').onclick = () => {
        window.basket[title]++;
        saveBasketToCookies(window.basket);
        renderBasket();
      };
      div.querySelector('.decrease').onclick = () => {
        window.basket[title]--;
        if (window.basket[title] <= 0) delete window.basket[title];
        saveBasketToCookies(window.basket);
        renderBasket();
      };
      div.querySelector('.remove').onclick = () => {
        delete window.basket[title];
        saveBasketToCookies(window.basket);
        renderBasket();
      };

      basketContainer.appendChild(div);
    });

    // кнопка оформления заказа создается только один раз
    if (!document.querySelector('.open-order-form')) {
      const orderButton = document.createElement('button');
      orderButton.textContent = 'Оформить заказ';
      orderButton.classList.add('order-btn', 'open-order-form');
      basketContainer.appendChild(orderButton);
    }
  }

  renderBasket();

  // открытие модалки корзины
  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('open-order-form')) {
      overlay.classList.add('active');
      form.classList.add('active');
    }
  });

  // закрытие модалки
  const closeBtn = document.getElementById('close-order-form');
  const closeModal = () => {
    overlay.classList.remove('active');
    form.classList.remove('active');
  };
  overlay.addEventListener('click', closeModal);
  if (closeBtn) closeBtn.addEventListener('click', closeModal);
});