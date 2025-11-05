function updateBasketButton(button, basket) {
  const productTitle = button.dataset.title;
  if (basket[productTitle]) {
    button.textContent = 'В корзине';
    button.classList.add('in-basket');
  } else {
    button.textContent = 'Купить';
    button.classList.remove('in-basket');
  }
}

function refreshAllBasketButtons(basket) {
  document.querySelectorAll('.basket').forEach(btn => {
    updateBasketButton(btn, basket);
  });
}


function renderBasket() {
  const basketContainer = document.getElementById('basket');
  if (!basketContainer) return;

  basketContainer.innerHTML = '';
  const titles = Object.keys(window.basket).filter(key => key !== 'generalCost');

  if (titles.length === 0) {
    basketContainer.innerHTML = '<p>Корзина пуста</p>';
    return;
  }

  let totalCost = 0;

  titles.forEach(title => {
    const [quantity, price] = window.basket[title];
    const unitPrice = price / quantity;
    const totalPrice = (quantity * unitPrice).toFixed(2);
    totalCost += parseFloat(totalPrice);

    const div = document.createElement('div');
    div.className = 'basket-item';
    div.innerHTML = `
      <span class="title">${title}</span>
      <span class="price">${totalPrice} BYN</span>
      <button class="decrease">−</button>
      <span class="quantity">${quantity}</span>
      <button class="increase">+</button>
      <button class="remove">🗑️</button>
    `;

    div.querySelector('.increase').onclick = () => {
      window.basket[title][0]++;
      const newQuantity = window.basket[title][0];
      const newTotalPrice = (newQuantity * unitPrice).toFixed(2);
      window.basket[title][1] = newTotalPrice;
      saveBasketToCookies(window.basket);
      renderBasket();
      refreshAllBasketButtons(window.basket);
    };

    div.querySelector('.decrease').onclick = () => {
      window.basket[title][0]--;
      const newQuantity = window.basket[title][0];
      if (newQuantity <= 0) {
        delete window.basket[title];
      } else {
        const newTotalPrice = (newQuantity * unitPrice).toFixed(2);
        window.basket[title][1] = newTotalPrice;
      }
      saveBasketToCookies(window.basket);
      renderBasket();
      refreshAllBasketButtons(window.basket);
    };

    div.querySelector('.remove').onclick = () => {
      delete window.basket[title];
      saveBasketToCookies(window.basket);
      renderBasket();
      refreshAllBasketButtons(window.basket);
    };

    basketContainer.appendChild(div);
  });

  window.basket.generalCost = totalCost.toFixed(2);
  const totalDiv = document.createElement('div');
  totalDiv.className = 'basket-total';
  totalDiv.innerHTML = `<strong>Итого: ${window.basket.generalCost} BYN</strong>`;
  basketContainer.appendChild(totalDiv);

  if (!document.querySelector('.open-order-form')) {
    const orderButton = document.createElement('button');
    orderButton.textContent = 'Оформить заказ';
    orderButton.classList.add('order-btn', 'open-order-form');
    basketContainer.appendChild(orderButton);
  }
}

document.addEventListener('DOMContentLoaded', () => {
window.basket = getBasketFromCookies();
renderBasket();

  const form = document.getElementById('order-form');
  const overlay = document.getElementById('overlay');



  document.querySelectorAll('.basket').forEach(button => {
    const productTitle = button.dataset.title;
    const productPrice = parseFloat(button.dataset.price.replace(',', '.')).toFixed(2);

    updateBasketButton(button, window.basket);

    button.addEventListener('click', () => {
      if (window.basket[productTitle]) {
        delete window.basket[productTitle];
      } else {
        window.basket[productTitle] = [1, productPrice];
      }

      saveBasketToCookies(window.basket);
      renderBasket();
      refreshAllBasketButtons(window.basket);
    });
  });

  renderBasket();

  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('open-order-form')) {
      overlay.classList.add('active');
      form.classList.add('active');
    }
  });

  const closeBtn = document.getElementById('close-order-form');
  const closeModal = () => {
    overlay.classList.remove('active');
    form.classList.remove('active');
  };
  overlay.addEventListener('click', closeModal);
  if (closeBtn) closeBtn.addEventListener('click', closeModal);
});

