function getViewedProducts() {
  const cookie = document.cookie.split('; ').find(row => row.startsWith('viewedProducts='));
  return cookie ? JSON.parse(decodeURIComponent(cookie.split('=')[1])) : [];
}

function saveViewedProduct(product) {
  let products = getViewedProducts();
  products = products.filter(p => p.id !== product.id);
  products.unshift(product);
  if (products.length > 7) {
    products = products.slice(0, 7);
  }
  document.cookie = `viewedProducts=${encodeURIComponent(JSON.stringify(products))}; path=/; max-age=604800`;
  }

function renderViewedProducts() {
  console.log('Куки:', document.cookie);
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

  products.forEach(product => {
    const card = document.createElement('div');
    card.className = 'product-card-catalog';

    const photoUrl = product.photo && product.photo.trim() !== ''
  ? product.photo
  : '/static/image/default-product.png';

    card.innerHTML = `
      <img src="${photoUrl}" alt="${product.title}">
      <a href="/product/${product.id}" class="product-title"
         data-id="${product.id}"
         data-title="${product.title}"
         data-price="${product.price}"
         data-description="${product.description}">
        <h3>${product.title}</h3>
      </a>
      <p>${product.description}</p>
      <p class="price">${product.price} BYN</p>
      <button type="button" class="basket" data-title="${product.title}" data-price="${product.price}">Купить</button>
    `;
    carousel.appendChild(card);
  });

  container.appendChild(carousel);

  const target = document.querySelector('#viewed-products-container');
  if (target) {
    target.appendChild(container);

    // Обработчики кнопок "Купить"
    container.querySelectorAll('.basket').forEach(button => {
      button.addEventListener('click', () => {
        const title = button.dataset.title;
        const price = button.dataset.price;
        console.log(`Добавлено в корзину: ${title} — ${price} BYN`);
        // Здесь можно вызвать функцию addToBasket(title, price)
      });
    });

    // Обработчики заголовков для сохранения в куки
    container.querySelectorAll('.product-title').forEach(link => {
      link.addEventListener('click', () => {
        const product = {
          id: link.dataset.id,
          title: link.dataset.title,
          price: link.dataset.price,
          description: link.dataset.description
        };
        saveViewedProduct(product);
      });
    });

  } else {
    console.warn('viewed-products-container не найден');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  renderViewedProducts();

  // Обработчики заголовков в каталоге
  document.querySelectorAll('.product-title').forEach(link => {
    link.addEventListener('click', () => {
      const product = {
        id: link.dataset.id,
        photo: link.dataset.photo,
        title: link.dataset.title,
        price: link.dataset.price,
        description: link.dataset.description
      };
      saveViewedProduct(product);
    });
  });
});
