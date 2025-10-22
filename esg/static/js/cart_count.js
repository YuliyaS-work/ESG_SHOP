document.addEventListener('DOMContentLoaded', () => {
  function updateCartCount() {
    const basket = getBasketFromCookies(); // читаем куки
    const count = Object.entries(basket)
  .filter(([key]) => key !== 'generalCost')
  .length; // считаем количество товаров по названиям
    const cartCountEl = document.getElementById('cart-count');
    if (cartCountEl) cartCountEl.textContent = count;
  }

  // обновляем сразу при загрузке страницы
  updateCartCount();
  // обновляем каждые 500ms на случай изменений на других вкладках
  setInterval(updateCartCount, 500);




  // находим все кнопки корзины
  //const buttons = document.querySelectorAll('.basket, .increase, .decrease, .remove');

  //buttons.forEach(button => {
    //button.addEventListener('click', () => {
      // небольшой таймаут, чтобы другие обработчики успели обновить куки
      //setTimeout(updateCartCount, 10);
    //});
  //});
});