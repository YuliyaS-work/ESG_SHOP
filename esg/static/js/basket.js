
document.addEventListener('DOMContentLoaded', () => {
  const basketContainer = document.getElementById('basket');
  const form = document.getElementById('order-form');
  const overlay = document.getElementById('overlay');
  let basket = getBasketFromCookies();

  function renderBasket() {
    basketContainer.innerHTML = '';

    const titles = Object.keys(basket);
    if (titles.length === 0) {
      basketContainer.innerHTML = '<p>Корзина пуста.</p>';
      return;
    }
//
    Object.entries(basket).forEach(([title, quantity]) => {
      const div = document.createElement('div');
      div.className = 'basket-item';
      div.innerHTML = `
        <span>${title}</span>
        <button class="decrease">−</button>
        <span class="quantity">${quantity}</span>
        <button class="increase">+</button>
        <button class="remove">🗑️</button>
      `;

      div.querySelector('.increase').onclick = () => {
        basket[title]++;
        saveBasketToCookies(basket);
        renderBasket();
      };

      div.querySelector('.decrease').onclick = () => {
        basket[title]--;
        if (basket[title] <= 0) {
          delete basket[title];
        }
        saveBasketToCookies(basket);
        renderBasket();
      };

      div.querySelector('.remove').onclick = () => {
        delete basket[title];
        saveBasketToCookies(basket);
        renderBasket();
      };

      basketContainer.appendChild(div);
    });

    const orderButton = document.createElement('button');
    orderButton.textContent = 'Оформить заказ';
    orderButton.onclick = () => {
      form.style.display = 'block';
      overlay.style.display = 'block';
    };
    basketContainer.appendChild(orderButton);
  }

  renderBasket();
});

