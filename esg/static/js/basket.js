//const sliderItemBasketBtn = document.querySelectorAll('.slider__item-basket');
//const headerBottomBasketCount = document.querySelector('.header__bottom-basket > p')
//
//
//
//let count = 0;
//headerBottomBasketCount.textContent = count
//
//sliderItemBasketBtn.forEach(item => {
//    item.addEventListener('click', () => {
//        count++
//        headerBottomBasketCount.textContent = count
//    })
//})

function getBasketFromCookies() {
  try {
    const cookie = document.cookie
      .split('; ')
      .find(row => row.startsWith('basket='));
    const parsed = cookie ? JSON.parse(decodeURIComponent(cookie.split('=')[1])) : {};
    return typeof parsed === 'object' && parsed !== null ? parsed : {};
  } catch (e) {
    console.warn('Ошибка чтения куки basket:', e);
    return {};
  }
}

function saveBasketToCookies(basket) {
  document.cookie = 'basket=' + encodeURIComponent(JSON.stringify(basket)) + '; path=/; max-age=2592000';
}

document.addEventListener('DOMContentLoaded', () => {
  const basketContainer = document.getElementById('basket');
  let rawBasket = getBasketFromCookies();
  let basket = {};

  Object.entries(rawBasket).forEach(([id, item]) => {
    if (item && typeof item.name === 'string') {
      basket[id] = {
        name: item.name,
        quantity: 1
      };
    }
  });

  function renderBasket() {
    basketContainer.innerHTML = '';
    Object.entries(basket).forEach(([id, item]) => {
      const div = document.createElement('div');
      div.className = 'basket-item';
      div.innerHTML = `
        <span>${item.name}</span>
        <button class="decrease">−</button>
        <span class="quantity">${item.quantity}</span>
        <button class="increase">+</button>
        <button class="remove">🗑️</button>
      `;

      div.querySelector('.increase').onclick = () => {
        item.quantity++;
        renderBasket();
      };

      div.querySelector('.decrease').onclick = () => {
        item.quantity--;
        if (item.quantity <= 0) {
          delete basket[id];
        }
        updateCookies();
        renderBasket();
      };

      div.querySelector('.remove').onclick = () => {
        delete basket[id];
        updateCookies();
        renderBasket();
      };

      basketContainer.appendChild(div);
    });
  }

  function updateCookies() {
    const updatedBasket = {};
    Object.entries(basket).forEach(([id, item]) => {
      updatedBasket[id] = { name: item.name };
    });
    saveBasketToCookies(updatedBasket);
  }

  renderBasket();
});