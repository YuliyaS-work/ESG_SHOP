function renderViewedProducts() {
  const products = getViewedProducts();

  if (products.length === 0) return;

// Создание шапки "Вы смотрели"
  const container = document.createElement('div');
  container.className = 'viewed-products';
  container.innerHTML = `
    <div style="text-align: center; margin-bottom: 10px; margin-top: 10px;">
      <h2 style="color: black; border-bottom: 2px solid #e6c200; display: inline-block; padding-bottom: 5px;">Вы смотрели</h2>
    </div>
  `;

// Создание блока для карточек
  const carousel = document.createElement('div');
  carousel.className = 'viewed-carousel';

// Загружает корзину из cookies, чтобы отобразить состояние кнопок "Купить"
 const basket = getBasketFromCookies();

// Создание карточки товара
  products.forEach(product => {
    const card = document.createElement('div');
    card.className = 'product-card-catalog';

    const photoUrl = product.photo && product.photo.trim() !== ''
      ? product.photo
      : '/static/image/default-product.png';

     const href = product.url || '/';

// Данные переданные через html
    card.innerHTML = `
      <img src="${photoUrl}" alt="${product.title}">
      <a href="${href}" class="product-title"
         data-id="${product.id}"
         data-title="${product.title}"
         data-product_title_translit = "${product.product_title_translit}"
         data-photo="${product.photo}"
         data-price="${product.price}"
         data-subrubric_title_translit="${product.subrubric_title_translit}"
         data-rubric_name_translit="${product.rubric_name_translit}"
         data-url="${href}">
        <h3>${product.title}</h3>
      </a>
      <p class="price">${product.price} BYN</p>
      <button type="button" class="basket" data-title="${product.title}" data-price="${product.price}">Купить</button>
    `;
// вставка карточки в контейнер
    carousel.appendChild(card);
  });
// вставка карусели в контейнер
  container.appendChild(carousel);

// вставляет блок в DOM
  const target = document.querySelector('#viewed-products-container');
  if (target) {
    target.innerHTML = '';
    target.appendChild(container);

// При клике на товар сохраняет как просомтренный
    container.querySelectorAll('.basket').forEach(button => {
      const title = button.dataset.title;
      const rawPrice = button.dataset.price;
      const price = parseFloat(rawPrice.replace(',', '.')).toFixed(2);

      // Установим начальное состояние кнопки
      const currentBasket = getBasketFromCookies();
      if (currentBasket[title]) {
        button.textContent = 'В корзине';
        button.classList.add('in-basket');
      } else {
        button.textContent = 'Купить';
        button.classList.remove('in-basket');
      }

      button.addEventListener('click', () => {
        const updatedBasket = getBasketFromCookies();

        if (updatedBasket[title]) {
          delete updatedBasket[title];
          button.textContent = 'Купить';
          button.classList.remove('in-basket');
        } else {
          updatedBasket[title] = [1, price];
          button.textContent = 'В корзине';
        button.classList.add('in-basket');
        }

        saveBasketToCookies(updatedBasket);
        window.basket = updatedBasket;

        if (typeof renderBasket === 'function') {
          renderBasket();
          refreshAllBasketButtons(window.basket);
        }
      });
    });
 // Обработка кликов по товарам, которые были сгенерированы динамически внутри блока "Вы смотрели".
    container.querySelectorAll('.product-title').forEach(link => {
      link.addEventListener('click', () => {
        const product = {
          id: link.dataset.id,
          photo: link.dataset.photo,
          title: link.dataset.title,
          product_title_translit: link.dataset.product_title_translit,
          price: link.dataset.price,
          subrubric_title_translit: link.dataset.subrubric_title_translit,
          rubric_name_translit: link.dataset.rubric_name_translit,
          url: link.dataset.url
        };
        saveViewedProduct(product);
      });
    });
  } else {
//    console.warn('viewed-products-container не найден');
  }
}

// Это для основного каталога, где карточки уже есть в HTML при загрузке страницы.
document.addEventListener('DOMContentLoaded', () => {
  renderViewedProducts();

  document.querySelectorAll('.product-title').forEach(link => {
    link.addEventListener('click', () => {

      const product = {
        id: link.dataset.id,
        photo: link.dataset.photo,
        title: link.dataset.title,
        product_title_translit: link.dataset.product_title_translit,
        price: link.dataset.price,
        subrubric_title_translit: link.dataset.subrubric_title_translit,
        rubric_name_translit: link.dataset.rubric_name_translit,
        url: link.dataset.url
      };
//      console.log('Сохраняем из каталога:', product);
      saveViewedProduct(product);
    });
  });
});

