function getBasketFromCookies() {
    try {
        const cookie = document.cookie
            .split('; ')
            .find(row => row.startsWith('basket='));
        return cookie ? JSON.parse(decodeURIComponent(cookie.split('=')[1])) : [] ;
    } catch (e) {
        console.warn('Ошибка чтения куки basket:', e);
        return [];
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

        // Если товар уже в корзине — отключаем кнопку
        if (basket.includes(productId)) {
            button.disabled = true;
            button.textContent = 'Уже в корзине';
        }

        button.addEventListener('click', () => {
            if (!basket.includes(productId)) {
                basket.push(productId);
                saveBasketToCookies(basket);
                button.disabled = true;
                button.textContent = 'Уже в корзине';
            }
        });
    });
});