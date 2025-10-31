function getViewedProducts() {
  const stored = localStorage.getItem('viewedProducts');
  return stored ? JSON.parse(stored) : [];
}

function saveViewedProduct(product) {
  const viewedProduct = {
    id: product.id,
    title: product.title,
    product_title_translit: product.product_title_translit,
    price: product.price,
    photo: product.photo,
    subrubric_title_translit: product.subrubric_title_translit,
    rubric_name_translit: product.rubric_name_translit

  };

  let products = getViewedProducts();
  products = products.filter(p => p.id !== viewedProduct.id);
  products.unshift(viewedProduct);
  if (products.length > 10) {
    products = products.slice(0, 10);
  }

  localStorage.setItem('viewedProducts', JSON.stringify(products));
}

function renderViewedProducts() {
  console.log('LocalStorage:', localStorage.getItem('viewedProducts'));
  const products = getViewedProducts();
  console.log('Просмотренные товары:', products);

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

  products.forEach(product => {
    const card = document.createElement('div');
    card.className = 'product-card-catalog';

    const photoUrl = product.photo && product.photo.trim() !== ''
      ? product.photo
      : '/static/image/default-product.png';

    const baseUrl = window.location.origin;
    const href = `${baseUrl}/esg.by/${product.rubric_name_translit}/${product.subrubric_title_translit}/${product.product_title_translit}/`;

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
         >
        <h3>${product.title}</h3>
      </a>
      <p class="price">${product.price} BYN</p>
      <button type="button" class="basket" data-title="${product.title}" data-price="${product.price}">Купить</button>
    `;
    carousel.appendChild(card);
  });

  container.appendChild(carousel);

  const target = document.querySelector('#viewed-products-container');
  if (target) {
    target.innerHTML = '';
    target.appendChild(container);

container.querySelectorAll('.basket').forEach(button => {
  const title = button.dataset.title;
  const rawPrice = button.dataset.price;
  const price = parseFloat(rawPrice.replace(',', '.')).toFixed(2);

  // Установим начальное состояние кнопки
  const currentBasket = getBasketFromCookies();
  if (currentBasket[title]) {
    button.textContent = 'Удалить из корзины';
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
      button.textContent = 'Удалить из корзины';
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


    container.querySelectorAll('.product-title').forEach(link => {
      link.addEventListener('click', () => {
        const product = {
          id: link.dataset.id,
          photo: link.dataset.photo,
          title: link.dataset.title,
          product_title_translit: link.dataset.product_title_translit,
          price: link.dataset.price,
          subrubric_title_translit: link.dataset.subrubric_title_translit,
          rubric_name_translit: link.dataset.rubric_name_translit

        };
        console.log('Сохраняем просмотренный товар:', product);
        saveViewedProduct(product);
      });
    });
  } else {
    console.warn('viewed-products-container не найден');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  renderViewedProducts();

  document.querySelectorAll('.product-title').forEach(link => {
    link.addEventListener('click', () => {

      const hrefParts = link.getAttribute('href').split('/');
      const rubric_name_translit = hrefParts[hrefParts.length - 4];
      const subrubric_title_translit = hrefParts[hrefParts.length - 3];
      const product_title_translit = hrefParts[hrefParts.length - 2];


      const product = {
        id: link.dataset.id,
        photo: link.dataset.photo,
        title: link.dataset.title,
        product_title_translit: product_title_translit,
        price: link.dataset.price,
        subrubric_title_translit: subrubric_title_translit,
        rubric_name_translit: rubric_name_translit

      };
      console.log('Сохраняем из каталога:', product);
      saveViewedProduct(product);
    });
  });
});

