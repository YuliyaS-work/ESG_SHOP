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
  const buttons = document.querySelectorAll('.basket');
  let basket = getBasketFromCookies();

  buttons.forEach(button => {
    const productId = button.dataset.id;
    const productTitle = button.dataset.title;

    if (basket[productId]) {
      button.disabled = true;
      button.textContent = 'Уже в корзине';
    }

    button.addEventListener('click', () => {
      if (!basket[productId]) {
        basket[productId] = { name: productTitle };
        saveBasketToCookies(basket);
        button.disabled = true;
        button.textContent = 'Уже в корзине';
      }
    });
  });
});