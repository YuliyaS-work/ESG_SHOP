//document.addEventListener("DOMContentLoaded", function() {
//  const modal = document.getElementById('productModal');
//  const modalContent = document.getElementById('modalProductContent');
//  const closeBtn = modal.querySelector('.modal-close');
//
//  // Универсальные селекторы карточек продуктов
//  const productSelectors = [
//    '.product-card-catalog',
//    '.product-card-single',
//    '.product-card-list'
//  ];
//
//  // Собираем все карточки
//  let productCards = [];
//  productSelectors.forEach(selector => {
//    document.querySelectorAll(selector).forEach(card => productCards.push(card));
//  });
//
//  productCards.forEach(card => {
//    card.addEventListener('click', (e) => {
//      // Предотвращаем переход по ссылке, если карточка использует <a>
//      if (e.target.tagName.toLowerCase() === 'a') e.preventDefault();
//
//      const titleEl = card.querySelector('h2, h3');
//      const imgEl = card.querySelector('img');
//      const descriptionEl = card.querySelector('p');
//      const priceEl = card.querySelector('.price');
//
//      const title = titleEl ? titleEl.innerText : '';
//      const img = imgEl ? imgEl.src : '';
//      const description = descriptionEl ? descriptionEl.innerText : '';
//      const price = priceEl ? priceEl.innerText : '';
//
//      // Подставляем контент в модалку
//      modalContent.innerHTML = `
//        <h2>${title}</h2>
//        <div class="product-image-container">
//          <img src="${img}" alt="${title}">
//        </div>
//        <p>${description}</p>
//        <p class="price">${price}</p>
//        <button class="basket" data-title="${title}">Купить</button>
//      `;
//
//      modal.style.display = 'flex';
//    });
//  });
//
//  // Закрытие модалки
//  closeBtn.addEventListener('click', () => modal.style.display = 'none');
//  modal.addEventListener('click', (e) => {
//    if (e.target === modal) modal.style.display = 'none';
//  });
//});