function createProductImage({ src, alt, fallback = '/static/image/default-product.png' }) {
  const img = document.createElement('img');
  img.alt = alt || '';

  img.onerror = () => {
    if (img.src !== fallback) {
      img.src = fallback;
      img.onerror = null; // защита от цикла для fallback
    }
  };

  img.src = src || fallback;
  return img;
}

async function renderViewedProducts() {
  const products = getViewedProducts();
  if (products.length === 0) return;

  const container = document.createElement('div');
  container.className = 'viewed-products';
  container.innerHTML = `
    <div style="text-align: center; margin-bottom: 10px; margin-top: 10px;">
      <h2 style="color: black; border-bottom: 2px solid #e6c200; display: inline-block; padding-bottom: 5px;">Вы смотрели</h2>
    </div>
  `;

  const carousel = document.createElement('div');
  carousel.className = 'viewed-carousel';

  const basket = getBasketFromCookies();

  for (const product of products) {
    const card = document.createElement('div');
    card.className = 'product-card-catalog';

    const href = product.url || '/';

    card.innerHTML = `
      <a href="${href}" class="product-title"
         data-id="${product.id}"
         data-title="${product.title}"
         data-product_title_translit="${product.product_title_translit}"
         data-photo="${product.photo}"
         data-price="${product.price}"
         data-subrubric_title_translit="${product.subrubric_title_translit}"
         data-rubric_name_translit="${product.rubric_name_translit}"
         data-url="${href}">
        <h3>${product.title}</h3>
      </a>
      <div class="card-bottom">
      <p class="price">${product.price} BYN</p>
      <button type="button" class="basket" data-title="${product.title}" data-price="${product.price}">Купить</button>
      </div>
    `;

    const hasPhoto = product.photo && product.photo.trim() !== '';
    const cacheBust = () => `?v=${Date.now()}`;
    const photoUrl = hasPhoto ? `${product.photo}${cacheBust()}` : '/static/image/default-product.png';

    const img = createProductImage({
      src: photoUrl,
      alt: product.title,
      fallback: '/static/image/default-product.png'
    });

    card.insertBefore(img, card.firstChild);
    carousel.appendChild(card);
  }

  container.appendChild(carousel);

  const target = document.querySelector('#viewed-products-container');
  if (!target) return;

  target.innerHTML = '';
  target.appendChild(container);

  // обработка кнопок корзины
  container.querySelectorAll('.basket').forEach(button => {
    const title = button.dataset.title;
    const rawPrice = button.dataset.price;
    const price = parseFloat(rawPrice.replace(',', '.')).toFixed(2);

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

  // сохранение просмотренных и мгновенное обновление
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

      // сразу перерисовываем блок "Вы смотрели"
      renderViewedProducts();
    });
  });
}

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
      saveViewedProduct(product);

      // здесь тоже обновляем
      renderViewedProducts();
    });
  });
});
