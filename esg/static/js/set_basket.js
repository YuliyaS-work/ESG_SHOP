// Для Тани 31, 34, 43, 49 указаны классы для css чтобы кнопка меняла цвет

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
    const productTitle = button.dataset.title;

    // Устанавливаем начальное состояние кнопки
    if (basket[productTitle]) {
      button.textContent = 'Удалить из корзины';
      button.classList.add('in-basket');
    } else {
      button.textContent = 'Купить';
      button.classList.remove('in-basket');
    }

    button.addEventListener('click', () => {
      if (basket[productTitle]) {
        // Удаление из корзины
        delete basket[productTitle];
        saveBasketToCookies(basket);
        button.textContent = 'Купить';
        button.classList.remove('in-basket');
      } else {
        // Добавление в корзину
        basket[productTitle] = 1;
        saveBasketToCookies(basket);
        button.textContent = 'Удалить из корзины';
        button.classList.add('in-basket');
      }
    });
  });
 });