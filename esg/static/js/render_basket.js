// чтобы кнопки купить автоматически обновлялись в корзине
  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('basket')) {
      const title = e.target.dataset.title;
      if (!title) return;

       // Устанавливаем начальное состояние кнопки
//    if (basket[productTitle]) {
//      button.textContent = 'Удалить из корзины';
//      button.classList.add('in-basket');
//    } else {
//      button.textContent = 'Купить';
//      button.classList.remove('in-basket');
//    }
      // если товара нет — добавляем, иначе увеличиваем количество
      if (window.basket[title]) {
        // Удаление из корзины
        delete basket[title];
        saveBasketToCookies(basket);
        button.textContent = 'Купить';
        button.classList.remove('in-basket');
      } else {
        window.basket[title] = [1, price];
        saveBasketToCookies(basket);
        button.textContent = 'Удалить из корзины';
        button.classList.add('in-basket');
      }

      saveBasketToCookies(window.basket);
      renderBasket();
    }
  });


